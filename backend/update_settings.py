#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 07:16:29 2018

@author: jur
"""
from pymongo import MongoClient
from database import db_update_dict, db_read_dict

client = MongoClient()
db = client.world    


settings = db_read_dict(db, 'settings')

print('Before:')
print(settings)

# do something
#settings['machines']['simplebot']['speed']= 0.1
settings['N']= 10

db_update_dict(db, 'settings', settings)

settings = db_read_dict(db, 'settings')

print('After:')
print(settings)
