#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 06:59:03 2018

@author: jur
"""
import time
import pandas as pd
import numpy as np

def db_clear(db):
    machines = db.machines
    machines.remove()
    grids = db.grids
    grids.remove()
    dicts = db.dicts
    dicts.remove()
    metrics = db.metrics
    metrics.remove()
#    metrics = db.metrics
#    metrics.remove()

#def db_replace_df(db, df):
#    machines = db.machines
#    for ix, row in df.iterrows():
#        machines.replace_one({'_id': int(ix)},
#                                   row.to_dict(),
#                                   upsert=True)

def db_insert_metrics(db, metric, machine_type, value):
    metrics = db.metrics
    metrics.insert_one({metric:{machine_type:(time.clock(),value)}})

def db_read_metrics(db):
    result=[]
    for metric in db.metrics.find():
        result.append(metric)
        
    return result

#def db_update_dict(db, key, d):
def db_update_dict(db, dict_name, dictionary):
    dicts = db.dicts
    dicts.update_one({'_id':dict_name},
                            {'$set':dictionary},
                            upsert=True)
 
#    for k,v in settings_dict.items():
##        settings.update_one({'_id':k},
#                            {'$set':v},
#                            upsert=True)
        
def db_read_dict(db, dict_name):
    dicts = db.dicts
    return dicts.find_one({'_id':dict_name})
#    dictionary = {}
#    for setting in settings.find()
#        settings_dict[setting['_id']]

def db_update_df(db, df):
    machines = db.machines
    for ix, row in df.iterrows():
        machines.update_one({'_id': int(ix)},
                                   {'$set': row.to_dict()},
                                   upsert=True)

def db_update_grid(db, _id, x, y, z):
    grids = db.grids
    grids.update_one(
            {'_id': _id},
            {'$set': {'x':x.tolist(),'y':y.tolist(),'z':z.tolist()}}, 
            upsert=True)


def db_read_df(db):
    machines = db.machines
    rows=[]
    for row in machines.find():
        rows.append(row)
    
    df=pd.DataFrame(rows)
    df.set_index('_id', inplace=True)
    
    return df

def db_read_grid(db, _id):
    grids = db.grids    
    grid_dict = grids.find_one({'_id':_id})
    x = np.array(grid_dict['x'])
    y = np.array(grid_dict['y'])
    z = np.array(np.array(grid_dict['z']))
    return x,y,z