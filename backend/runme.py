#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 15:34:35 2018

@author: jur
"""
#import subprocess
import webbrowser

import multiprocessing
import simpleserver
import world
import machines
import views



if __name__ == '__main__':
    targets = [world.main, machines.main, views.main]
    
    multiprocessing.set_start_method('spawn')
    
    for target in targets:
        p = multiprocessing.Process(target=target)
        p.start()
        #p.join()

#subprocess.call(['python', 'simpleserver.py'])
#webbrowser.open('http://localhost:7000/testwebapp.html')

