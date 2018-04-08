#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 11:12:20 2018

@author: morten
"""

from settings import tokens#,master_keys
from utils import dist, rnd_vec, update_metrics
from time import sleep

class roguebot:
    def __init__ (self, radius=5):
        self.radius=0.9

def set_df(df, settings, metrics, db):
    machine_type = __name__.split('.')[-1]
    S, MIN_D, MAX_X, MAX_Y = (settings[k] for k in ('S', 'MIN_D', 'MAX_X', 'MAX_Y'))
    s = (df['machine_type']==machine_type)
    
    if any(s):
        
        speed, reward, penalty = (settings['machines'][machine_type][k] for k in ('speed', 'reward', 'penalty'))
        #define ix
        
        
        col_x_trg, col_y_trg = 'x_trg' , 'y_trg'
        # get coördinates from nearest robot ans set target
        
        for ix, row in df.loc[s].iterrows():
            
            neighbour_ix = dist(row.x,row.y,df[df.index!=ix].x,df[df.index!=ix].y).idxmin()
            #defining neighbours location
            df.loc[ix,'ix_near'] = int(neighbour_ix)
            df.loc[ix,'x_near'] = df.loc[neighbour_ix,'x']
            df.loc[ix,'y_near'] = df.loc[neighbour_ix,'y']
        
        #reward when bullying nearest neighbour
        reward = 1.0 
        offset = 1.0
        df.loc[s,'ds'] = reward * dist(df.loc[s,'x'], df.loc[s,'y'], df.loc[s,col_x_trg], df.loc[s,col_y_trg])
        df.loc[s, 'dx'] = df.loc[s,'x_near'] - df.loc[s, 'x' ]  #distance to nearest neighbour #trg is 
        df.loc[s, 'dy'] = df.loc[s, 'y_near'] - df.loc[s, 'y'] + offset 
        
        #penalty when away by more then 20 units
        penalty = 1.0
        df.loc[s,'ds1'] = penalty * dist(df.loc[s,'x'], df.loc[s,'y'], df.loc[s,'x_near'], df.loc[s,'y_near'])
        df.loc[s, 'dx1'] = df.loc[s, 'x_near'] - df.loc[s, 'x']
        df.loc[s, 'dy1'] = df.loc[s, 'y_near'] - df.loc[s, 'y']
    
        # speed is max(the remaining dist, S) ds is always positive
        selection = s & (df['ds']>0)
        #if not selection.empty:
        fr = df.loc[selection]
        df.loc[selection,'u'] = fr.ds.clip_upper(speed) * fr['dx']/fr['ds']
        df.loc[selection,'v'] = fr.ds.clip_upper(speed) * fr['dy']/fr['ds']
    
        df.loc[selection,'u1'] = fr.ds.clip_upper(speed) * fr['dx1']/fr['ds1']
        df.loc[selection,'v1'] = fr.ds.clip_upper(speed) * fr['dy1']/fr['ds1']
        
    
    
    
    
   
#get location of simplebots from dataframe







