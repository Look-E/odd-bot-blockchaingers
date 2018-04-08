# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 12:27:15 2018

@author: PietersmaJ

TODO: 
    1. add gradient field 
    2. turn into server 
    3. add 3djs visualization 
    4. collisions 
    5. reference frame
    6.....

"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from mpl_toolkits.mplot3d import Axes3D


from pymongo import MongoClient
from database import db_read_df, db_read_grid, db_read_dict
from settings import SETTINGS
   
# setup database
MAX_X, MAX_Y, R,  MOVIE = (SETTINGS[k] for k in ('MAX_X', 'MAX_Y', 'R', 'MOVIE'))
client = MongoClient()
db = client.world    

df = db_read_df(db)
xi, yi, zi = db_read_grid(db, 'world')

# scatter plot
fig, ax = plt.subplots(figsize=(10,7))
ax.set_xlim(0, MAX_X)
ax.set_ylim(0, MAX_Y)
scat = ax.scatter(x=df['x'],y=df['y'], marker='o')#, animated=True)
scat_trg = ax.scatter(x=[],y=[],marker='+')#, animated=True)
# contour
contour = ax.contour(xi, yi, zi)#, levels=np.linspace(0,1,num=10))
# mesh
fig3d = plt.figure(figsize=(10,7))
ax3d = fig3d.add_subplot(111,projection='3d')
xm,ym = np.meshgrid(xi,yi)
ax3d.plot_wireframe(xm,ym,zi)

ax3d.set_zlim3d(-1.0,1.0)

def update(frame_number):
    global contour #, utility
    
#    settings = db_read_dict(db, 'settings')
#    MAX_X, MAX_Y, R,  MOVIE = (SETTINGS[k] for k in ('MAX_X', 'MAX_Y', 'R', 'MOVIE'))
    # read machines information 
    df = db_read_df(db)
    xi, yi, zi = db_read_grid(db, 'world')
    
    # velocity has been set by machines
    if 'x_trg' in df.columns and 'y_trg' in df.columns:

        scat.set_offsets(df[['x','y']].values)
        scat_trg.set_offsets(df[['x_trg','y_trg']].values)
#    contour.set_array(utility)
    #scat.set_offsets(np.concatenate([df[['x','y']].values,df[['x_trg','y_trg']].values]))
    for c in contour.collections:
        c.remove()
    
    xm,ym = np.meshgrid(xi,yi)
    contour = ax.contour(xi, yi, zi)#, leve

    for c in ax3d.collections:
        c.remove()
    ax3d.plot_wireframe(xm,ym,zi)
    
    return scat, scat_trg, contour

    
# repeat or make movie        
ani = anim.FuncAnimation(fig,update,frames=R,  repeat=not MOVIE, interval=500)

if MOVIE:
    ani.save(BEHAVIOUR+'.mp4')
    
ani3d = anim.FuncAnimation(fig3d,update,frames=R,  repeat=not MOVIE, interval=500)

if MOVIE:
    ani3d.save(BEHAVIOUR+'3D.mp4')

        