#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 20:19:39 2018

@author: jur
"""
        
def set_df(df, settings, metrics, db):
    machine_type = __name__.split('.')[-1]
    S, MIN_D, MAX_X, MAX_Y, USE_BIGCHAINDB = (settings[k] for k in 
                                              ('S', 'MIN_D', 'MAX_X', 'MAX_Y', 'USE_BIGCHAINDB'))
    speed, reward, penalty = (settings['machines'][machine_type][k] for k in ('speed', 'reward', 'penalty'))
    
