#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Here is performed the main loop of simulation

to clear all data, execute `%reset` in Ipython console
"""

#%%
import generator_positions as genpos
import class_vortex as genvortex
import generator_props as genprops
import stepping

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def genPositions(shape, *args):
    positions = genpos.generate_positions(shape, *args)
    return positions
    

def addProperties(segments, v_s):
    genprops.add_properties(segments, v_s)
#%%
## INITIAL POSITIONS INIT
shape = 'ring'
N = 100
center = [0,0,0]
radius = 0.001

positions = genpos.generate_positions(shape, N, center, radius)
#%%
## VORTEX CREATION
vortex = genvortex.Vortex(positions)

# fixing neigbours
vortex.segments[0]['backward'] = N - 1
vortex.segments[N-1]['forward'] = 0

# adding properties
v_s = np.zeros(3)
vortex.segments = genprops.add_properties(vortex.segments, v_s)

#%%
iters = 10
dt=0.1

mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure()
ax = fig.gca(projection='3d')
for i in range(iters):
    print('Starting step {}'.format(i))
    ax.scatter(vortex.getAllAxisCoords(0), 
           vortex.getAllAxisCoords(1),
           vortex.getAllAxisCoords(2), 
           label='ring')
    stepping.update_coords(vortex.segments, dt)
    print(vortex.getCoords(1))
    
#ax.legend()
plt.show()