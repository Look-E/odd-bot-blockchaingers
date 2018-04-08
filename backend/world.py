# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 12:27:15 2018

@author: PietersmaJ

TODO: 
    1. add gradient field 
    2. turn into server 
    3. add 3djs visualization 
    4. collisions 
    5. reference frame
    6.....

"""
import time
import numpy as np
import pandas as pd 

from scipy.interpolate import griddata

from pymongo import MongoClient
from database import db_read_df, db_update_df, db_clear, db_update_grid, db_update_dict, db_read_dict, db_insert_metrics, db_read_metrics
from settings import SETTINGS
from utils import rnd_vec, dist
#import socket

#from socket_functions import sock_send_df, sock_send_grid

#alex
from bigchaindb_driver.crypto import generate_keypair
#alex end

from machine_types import simplebot, roguebot, wigglebot
machine_modules = (simplebot, roguebot, wigglebot)


def cost_function(df, selection, machine_id, settings):
    MAX_X, MAX_Y= settings['MAX_X'], settings['MAX_Y']
    method = settings['INTERPOLATION']

    if 'ix_near' in df.columns:

        neighbour_id = df.loc[machine_id,'ix_near']

        df.loc[int(neighbour_id),'cost'] = 1.0


    xi=np.linspace(0,MAX_X)
    yi=np.linspace(0,MAX_Y)
    
    
    fr= df.loc[selection]
    reward = np.zeros(len(fr))
    
    reward[machine_id]=-1.0
    
    #h = np.array([*fr.cost.values, *reward])
    #if not all(h==0.0):
    try:
        zi = griddata((np.array([*fr.x.values, *fr.x_trg.values]), np.array([*fr.y.values, *fr.y_trg.values])), 
                      np.array([*fr.cost.values, *reward]),
                      (xi[None,:],yi[:,None]), 
                      method=method,
                      fill_value=0.0)
    except:   
        zi =np.zeros(len(xi))
    return xi, yi, zi
    
#async def send_data(websocket, path):
#def main():
# setup database



def world_gen(database_name='world')    :

    client = MongoClient()
    db = client[database_name]
    db_clear(db)
    
    t=time.clock()
    metrics={
        'collisions':{'simplebot':(t,0), 'wigglebot':(t,0)},
        'pickups':{'simplebot':(t,0), 'wigglebot':(t,0)},
        'dropoffs':{'simplebot':(t,0), 'wigglebot':(t,0) },
        }

    #    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #    sock.connect((HOST, PORT))
    

    
    # settings
    N = SETTINGS['N']
    MAX_X = SETTINGS['MAX_X']
    MAX_Y = SETTINGS['MAX_Y']
    
    db_update_dict(db, 'settings', SETTINGS)
    
    
    # metrics
#    t = time.clock()
#    metrics = {'collisions':[(t,0)],
   #                          'pickups':[(t,0)],
    #                         'dropoffs':[(t,0)]}
#    db_update_dict(db, 'metrics', metrics)
#    update_metrics(db, 'collisions',0)   
#    db_insert_metrics(db, 'pickups',0)   
#    db_insert_metrics(db, 'dropoffs',0)   
       
    
    #%%
    
    df = pd.DataFrame(index=range(N), 
                      data={'x': rnd_vec(N,MAX_X),
                            'y': rnd_vec(N,MAX_Y)})
    
    
    
    # alex      
    df['private_key'] = 'empty' # bigchaindb private key for each unique robot
    df['public_key'] = 'empty' # bigchaindb public key for each unique robot
    df['state'] = 'empty' # intial state of the robot. this state is later stored in metadata tag in blockchaindb 
    for ix, row in df.iterrows():
        current_keypair = generate_keypair()
        private_key = current_keypair.private_key     
        public_key = current_keypair.public_key     
        df.loc[ix,'private_key'] = private_key
        df.loc[ix,'public_key'] = public_key
    # alex end
        
    # blender specific columns
    df['blender_name'] = ''
    df['blender_type'] = 'object'
    df.loc[0,'blender_name'] = 'car.001'
    
    #df.loc[:N/2,'machine_type'] = 'simplebot'
    df['machine_type'] = 'simplebot'#'simplebot'#'wigglebot'#
    #MORTEN  BEGIN  
    df.loc[N-1,'machine_type'] = 'roguebot' #overwriting 1 so one rogue node availlable
    #MORTEN END


    df['radius'] = 0.9
    df['collision'] = False
    df['cost'] = 0.0
    #df['u']=0.0
    #df['v']=0.0
    
    df['x_trg'] = rnd_vec(N,MAX_X)
    df['y_trg'] = rnd_vec(N,MAX_Y)
        
    db_update_df(db, df)
    
    
    
    while True:
        
        # read machines information 
        # get rid of nans
        df = db_read_df(db)
        settings = db_read_dict(db, 'settings')
        tokens = {}
#alex
#tokens['app_id'] = '4a33bc96'
#tokens['app_key'] = '5e9699fbe0c5bca83d35e3a7e63ba1c1'
#jur
#tokens['app_id'] = 'dbd40a9c'
#tokens['app_key'] = 'a8062ad9546eba03f4f61ad7f6d4afac'
#from bigchaindb_driver.crypto import generate_keypair
#master_keys = generate_keypair()

        for machine_module in machine_modules:
            machine_module.set_df(df, settings, metrics, db)
        
        #update settings for failing bigchaindb
        db_update_dict(db,'settings', {'USE_BIGCHAINDB':settings['USE_BIGCHAINDB']})
        
        # velocity has been set by machines
        if 'u' in df.columns and 'v' in df.columns:
            
            selection = ~df.u.isna() & ~df.v.isna()
            
            df.loc[selection, 'x_new'] = df.loc[selection, 'x'] + df.loc[selection, 'u']
            df.loc[selection, 'y_new'] = df.loc[selection, 'y'] + df.loc[selection, 'v']
            
            for ix, row in df.iterrows():
                fr=df[df.index!=ix]
                df.loc[ix,'collision'] = any(dist(row.x_new,row.y_new,fr.x_new,fr.y_new)<=(fr.radius+row.radius))
            
            collisions = len(df[df.collision])
            if collisions>0:
                print('collisions', collisions)
            
            df.loc[~df.collision,'x'] = df.loc[~df.collision,'x_new']
            df.loc[~df.collision,'y'] = df.loc[~df.collision,'y_new']
            
            db_update_df(db, df.loc[selection])
        
        #xi, yi, zi=fn_cost(df, method=INTERPOLATION)
            # only if we have a target
            xi, yi, zi=cost_function(df,selection, 0, settings)
        
            db_update_grid(db, 'world', xi, yi, zi)
        
            grid = {'world':{'x':xi,'y':yi,'z':zi}}
        
        #metrics = db_read_metrics(db)
        
        yield df, grid, metrics

if __name__ == '__main__':
    for df, grid, metrics in world_gen():
        pass

    
