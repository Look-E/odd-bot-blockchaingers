#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 20:19:39 2018

@author: jur
"""
#from settings import tokens,master_keys
from utils import dist, rnd_vec, update_metrics
# alex - needs to be in bigchaindb
from bigchainactions import createAsset, transferAsset
from settings import master_receiver_private_key, master_receiver_public_key 
from settings import master_sender_private_key,master_sender_public_key

from time import sleep
import urllib3

# alex end 

#class SimpleBot:
    
#    def __init__(self, radius=5.0):
#        self.radius = radius
        
def set_df(df, settings, metrics, db):
    machine_type = __name__.split('.')[-1]
    S, MIN_D, MAX_X, MAX_Y, USE_BIGCHAINDB = (settings[k] for k in 
                                              ('S', 'MIN_D', 'MAX_X', 'MAX_Y', 'USE_BIGCHAINDB'))
    s = (df['machine_type']==machine_type)
    
    speed, reward, penalty = (settings['machines'][machine_type][k] for k in ('speed', 'reward', 'penalty'))
    
#    print('********************************', speed, reward, penalty)
    
    
    col_x_trg, col_y_trg = 'x_trg', 'y_trg'                

#    df.loc[s,'x_near'] = df.loc[s,'x_trg']
#    df.loc[s,'y_near'] = df.loc[s,'y_trg']
    for ix, row in df.loc[s].iterrows():
        #print(i,r)
        neighbour_ix = dist(row.x,row.y,df[df.index!=ix].x,df[df.index!=ix].y).idxmin()
        # if I am not the nearest set nearest as target
#        if ix!=neighbour_ix:
        df.loc[ix,'ix_near'] = int(neighbour_ix)
        df.loc[ix,'x_near'] = df.loc[neighbour_ix,'x']
        df.loc[ix,'y_near'] = df.loc[neighbour_ix,'y']
   
    # reward
    #reward = 1.0
    df.loc[s,'ds'] = dist(df.loc[s,'x'], df.loc[s,'y'], df.loc[s,col_x_trg], df.loc[s,col_y_trg])
    df.loc[s,'dx'] = df.loc[s,col_x_trg] - df.loc[s,'x']
    df.loc[s,'dy'] = df.loc[s,col_y_trg] - df.loc[s,'y']

    # penalty
    #penalty = 1.0#1.0
    df.loc[s,'ds1'] =  dist(df.loc[s,'x'], df.loc[s,'y'], df.loc[s,'x_near'], df.loc[s,'y_near'])
    df.loc[s,'dx1'] = -(df.loc[s,'x_near'] - df.loc[s,'x'])
    df.loc[s,'dy1'] = -(df.loc[s,'y_near'] - df.loc[s,'y'])

   
    # speed is max(the remaining dist, S) ds is always positive
    selection = s & (df['ds']>=MIN_D)
    #if not selection.empty:
    fr = df.loc[selection]
    df.loc[selection,'u'] = fr.ds.clip_upper(reward*speed) * fr['dx']/fr['ds']
    df.loc[selection,'v'] = fr.ds.clip_upper(reward*speed) * fr['dy']/fr['ds']

    #df.loc[selection,'u1'] = fr.ds1.clip_upper(penalty*speed) * fr['dx1']/(fr['ds1']**3)
    #df.loc[selection,'v1'] = fr.ds1.clip_upper(penalty*speed) * fr['dy1']/(fr['ds1']**3)

    df.loc[selection,'u1'] = (1.0/ (fr['dx1']**2)).clip_upper(penalty*speed)
    df.loc[selection,'v1'] = (1.0/ (fr['dy1']**2)).clip_upper(penalty*speed)


     # TODO: doesn't really work
    #selection = s & (df['ds']<MIN_Dspeed)
    df.loc[selection,'u'] += df.loc[selection,'u1']
    df.loc[selection,'v'] += df.loc[selection,'v1']
    
    # on collision turn left
    selection = s & (df['collision'])
#    fr = df.loc[selection]
    # choose random vector, noise evolution
#    df.loc[selection, 'u']=rnd_vec(len(df.loc[selection]),2.0)-1.0
#    df.loc[selection, 'v']=rnd_vec(len(df.loc[selection]),2.0)-1.0
#    df.loc[selection, 'ds']=(df.loc[selection, 'u']**2 + df.loc[selection, 'v']**2)**0.5
#    df.loc[selection,'u'] = fr.ds.clip_upper(speed) * fr['u']/fr['ds']
#    df.loc[selection,'v'] = fr.ds.clip_upper(speed) * fr['v']/fr['ds']
#    df.loc[selection,'u'] = fr.ds.clip_upper(speed) * fr['u']/fr['ds']
#    df.loc[selection,'v'] = fr.ds.clip_upper(speed) * fr['v']/fr['ds']
    
    u = df.loc[selection, 'v']
    v = -df.loc[selection, 'u']
    df.loc[selection, 'u'] = u
    df.loc[selection, 'v'] = v
    update_metrics(db, metrics, 'collisions', machine_type, len(df.loc[selection]))

    # determine if target is reached and set new target
    # new target should come from blockchain
    selection = s & (df['ds'].abs()<MIN_D)
    #if not selection.empty:
    l = len(df.loc[selection])
    if l>0:
        print('targets reached', l)
    df.loc[selection,'x_trg'] = rnd_vec(l,MAX_X)
    df.loc[selection, 'y_trg'] = rnd_vec(l,MAX_Y)

# alex
# this code uses simple binary state change to describe whether the robot is carrying
# an asset (for example energy or a parcel or whatever) 
    update_metrics(db, metrics, 'pickups', machine_type, len(df[selection & (df['state']=='empty')]))
    update_metrics(db, metrics, 'dropoffs', machine_type, len(df[selection & (df['state']=='carry')]))
    
    for ix, row in df.loc[selection].iterrows(): # for each bot that reached a new waypoint change its behaviour
        if df.loc[ix,'state'] == 'empty':
            print('empty bot changed to carry')
            # alex adjusted
            currentBot = df.loc[ix]                                
            if USE_BIGCHAINDB:
                createAsset(master_sender_private_key,master_sender_public_key) # mockup sender initialization, creation of paackage to take for bot
                transferAsset(master_sender_public_key,master_sender_private_key,currentBot.public_key,currentBot.private_key) # transfer parcel from master_sender to current robot
            df.loc[ix,'state'] = 'carry'
        elif df.loc[ix,'state'] == 'carry':
            print('carry bot changed to empty')
            # alex adjusted
            currentBot = df.loc[ix]                
            if USE_BIGCHAINDB:
                transferAsset(currentBot.public_key,currentBot.private_key, master_receiver_public_key,master_receiver_private_key) # transfer parcel from current robot to master receiver
            df.loc[ix,'state'] = 'empty'
                
# alex end       