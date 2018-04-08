#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 20:19:39 2018

@author: jur
"""
from settings import BEHAVIOUR, S, MIN_D, MAX_X, MAX_Y
from utils import dist, rnd_vec


#class SimpleBot:
    
#    def __init__(self, radius=5.0):
#        self.radius = radius
        
def set_df(df):
    #print(__name__)
    s = (df['machine_type']==__name__.split('.')[-1])
    
#    if not s.empty:
        
        #fr = df.loc[]
    #    df['radius'] = self.radius
        #df.loc[s, 'by'] = df.loc[s, 'y'] + self._box[0]
    #        fr['by'] = fr['y'] + self._box[1]
     #       fr['bz'] = df['z'] + self._box[2]
    
    df.loc[s,'radius']     = 0.05
     
    if BEHAVIOUR == 'solo':
        # calc distance velocities x_target - x
        #df['ds'] = dist(df['x'], df['y'], df['x_trg'], df['y_trg'])
        #df['dx'] = df['x_trg'] - df['x']
        #df['dy'] = df['y_trg'] - df['y']
        col_x_trg, col_y_trg = 'x_trg', 'y_trg'                

    elif BEHAVIOUR == 'nearest_target':
        # we travel via the robot nearest to target if any
        # for default we take original target
        df.loc[s,'x_near'] = df.loc[s,'x_trg']
        df.loc[s,'y_near'] = df.loc[s,'y_trg']
        for ix, row in df.loc[s].iterrows():
            #print(i,r)
            neighbour_ix = dist(row.x_trg,row.y_trg,df.x,df.y).idxmin()
            # if I am not the nearest set nearest as target
            if ix!=neighbour_ix:
                df.loc[ix,'x_near'] = df.loc[neighbour_ix,'x']
                df.loc[ix,'y_near'] = df.loc[neighbour_ix,'y']
        
        col_x_trg, col_y_trg = 'x_near', 'y_near'
    elif BEHAVIOUR == 'gradient':
        #utility = fn_cost(utility, df)
        #fn_cost(df)                
        # dummy                
        col_x_trg, col_y_trg = 'x_trg', 'y_trg'                

    else:
        raise NotImplemented
 
    df.loc[s,'ds'] = dist(df.loc[s,'x'], df.loc[s,'y'], df.loc[s,col_x_trg], df.loc[s,col_y_trg])
    df.loc[s,'dx'] = df.loc[s,col_x_trg] - df.loc[s,'x']
    df.loc[s,'dy'] = df.loc[s,col_y_trg] - df.loc[s,'y']
   
    # speed is max(the remaining dist, S)
    selection = s & (df['ds']>0)
    #if not selection.empty:
    fr = df.loc[selection]
    df.loc[selection,'u'] = fr.ds.clip_upper(S) * fr['dx']/fr['ds']
    df.loc[selection,'v'] = fr.ds.clip_upper(S) * fr['dy']/fr['ds']
    
    # on collision turn left
    selection = s & (df['collision'])
    u = df.loc[selection, 'v']
    v = -df.loc[selection, 'u']
    df.loc[selection, 'u'] = u
    df.loc[selection, 'v'] = v

    # determine if target is reached and set new target
    # new target should come from blockchain
    selection = s & (df['ds'].abs()<MIN_D)
    #if not selection.empty:
    l = len(df.loc[selection])
    if l>0:
        print('targets reached', l)
    df.loc[selection,'x_trg'] = rnd_vec(l,MAX_X)
    df.loc[selection, 'y_trg'] = rnd_vec(l,MAX_Y)

        
        
        