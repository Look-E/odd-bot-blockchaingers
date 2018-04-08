#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 07:14:08 2018

@author: jur
"""
SETTINGS ={
    'N' : 5,#100,#100,#100#100#3#10
    'MAX_X' : 60,#-20#60
    'MAX_Y' : 60,#-20#30
    'S' : 1,#.1#1.0#0.1#1.0#.1#2 # fixed speed
    'MIN_D' : 0.01,#1e-4, # precision / minimal measurable distance
    'INTERPOLATION' : 'linear', #'cubic'#'linear' or 'nearest'  
    'R' :100,#200#00 # nr of runs

    'USE_BIGCHAINDB' : False,

#BEHAVIOUR = 'nearest_target'
#BEHAVIOUR = 'solo'
#BEHAVIOUR = 'gradient'

    'MOVIE' : False, #False|True
    
    'machines':{'simplebot':{'speed':1.0,'reward':1.0,'penalty':1.0},
                'roguebot':{'speed':1.0,'reward':1.0,'penalty':1.0},
                'wigglebot':{'speed':1.0,'reward':1.0,'penalty':1.0}}
                }

#INTERPOLATION = 'nearest'tokens = {}
#alex
#tokens['app_id'] = '4a33bc96'
#tokens['app_key'] = '5e9699fbe0c5bca83d35e3a7e63ba1c1'
#jur
#tokens['app_id'] = 'dbd40a9c'
#tokens['app_key'] = 'a8062ad9546eba03f4f61ad7f6d4afac'
#from bigchaindb_driver.crypto import generate_keypair
#master_keys = generate_keypair()


HOST = 'localhost'
#HOST = '10.1.2.15'
PORT = 10000

# alex
# initialize object which all robots will use to communicate to the 
# global DB. These setttings are derived from the test server so 
# for each user registration this is different (set the app_id and app_key)
# you need to register on boghchaindb and get this information under
# "connect in python", which you can find on https://testnet.bigchaindb.com/

tokens = {}
#alex
#tokens['app_id'] = '4a33bc96'
#tokens['app_key'] = '5e9699fbe0c5bca83d35e3a7e63ba1c1'
#jur
tokens['app_id'] = 'dbd40a9c'
tokens['app_key'] = 'a8062ad9546eba03f4f61ad7f6d4afac'
from bigchaindb_driver.crypto import generate_keypair

master_receiver_private_key='CiU56eNwScL7S89gAUUh1xfiub4nhiopF6sVa85HTvK7'
master_receiver_public_key='kRkyL8X2AavMvcPB2NGPGFr1S8BvYeTZfQ8kTeZM1X4'

master_sender_private_key = 'tSc2YBW4gYUzXWeoUB8QmB3D5BpezGrTCvaUCCowAUx'
master_sender_public_key = 'CXBUJeknCHxVe59vgojq4TKz341VyLokkNwVVH5ceQkX'

# alex end
