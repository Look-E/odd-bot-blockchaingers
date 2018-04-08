#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 07:37:35 2018

@author: jur
"""

import socket, pickle
#from struct import pack
#import pickle

HOST = 'localhost'
PORT = 10000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((HOST, PORT))
#arr = ([1,2,3,4,5,6],[1,2,3,4,5,6])
#data_string = pickle.dumps(arr)
#s.send(pack('ddd',1.0,1.0,1.0))
s.send(pickle.dumps({'x':1.0,'y':1.0,'z':1.0}))