#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 06:45:16 2018

@author: jur
"""
from time import sleep

from pymongo import MongoClient
import pandas as pd

from database import db_read_df, db_update_df
from utils import rnd_vec, dist
from settings import N, MAX_X, MAX_Y, BEHAVIOUR, MIN_D, S


from machine_types import simplebot
machine_modules = (simplebot,)


#%%
# setup database
client = MongoClient()
db = client.world

# set initial target and speed
df = db_read_df(db)
# initialize rest target positions and velocities
df['x_trg'] = rnd_vec(N,MAX_X)
df['y_trg'] = rnd_vec(N,MAX_Y)

# TODO reference frame, z and w
df['u'] = 0     # speed in x direction (TODO: reference frome)
df['v'] = 0     # speed in y direction (TODO: reference frome)

db_update_df(db, df)

while True:
    # get positions
    df = db_read_df(db)
    # do apply ??
    for machine_module in machine_modules:
        machine_module.set_df(df)
        
        
        

    db_update_df(db,df)
    
#    print(df.head(1))
    #sleep(0.01)
