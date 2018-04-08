#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 07:15:28 2018

@author: jur
"""
import time
import numpy as np
from database import db_insert_metrics,db_read_metrics

from pymongo import MongoClient

def rnd_vec(n, mx):
    return np.random.rand(n)*mx


def dist(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y1-y0)**2)**0.5

def update_metrics(db, metrics, metric_name, machine_type, value):
    if value>0:
        t = time.clock()
        #metric = metrics.get(metric_name,{})
        #machine_type = metric.get(machine_type,{})
        #machine_type[t] = value
        #metrics[metric_name][machine_type][t] = value
        
#        if metrics=={}:
            
        last = metrics[metric_name][machine_type][1]
        metrics[metric_name][machine_type]=(t,last+value)
        db_insert_metrics(db, metric_name, machine_type, last+value)
    

def dump_metrics():
    client = MongoClient()
    db = client.world
    return db_read_metrics(db)