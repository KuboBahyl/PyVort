#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Here is performed the main loop of simulation.
To clear all data, execute `%reset` in ipython console
"""
#%%
###################
###   IMPORTS   ###
###################

# Libraries
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# Objects, functions
import generator_positions
import class_vortex
import generator_props
import stepping

# Basic operations init
def createPositions(shape, pieces, *args):
    return generator_positions.generate_positions(shape, pieces, *args)

def createVortex(positions):
    return class_vortex.Vortex(positions)

def addProperties(segments, velocity_superfluid):
    return generator_props.add_properties(segments, velocity_superfluid)

def makeStep(segments, dt):
    return stepping.update_coords(segments, dt)

#%%
##################################
###   SINGLE VORTEX CREATION   ###
##################################

# Initial position
shape = 'ring'
pieces = 100
center = [0,0,0]
radius = 0.001

positions = createPositions(shape, pieces, center, radius)

# Vortex init
vortex = createVortex(positions)

# Fixing boundary neighbours
vortex.segments[0]['backward'] = pieces - 1
vortex.segments[pieces-1]['forward'] = 0

# Adding properties - first and second derivation, velocities (superfluid)
velocity_superfluid = np.zeros(3)
addProperties(vortex.segments, velocity_superfluid)

#%%
##########################
###   TIME EVOLUTION   ###
##########################

# Time steps and steplength
steps = 10
dt=0.1

#mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')
for i in range(steps):
    
    # Plotting
    #if (i%10==0): 
    print('Starting step {}'.format(i))
    ax.plot(vortex.getAllAxisCoords(0), 
           vortex.getAllAxisCoords(1),
           vortex.getAllAxisCoords(2), 
           label='ring',
           color='blue')
    
    # vortex evolution
    makeStep(vortex.segments, dt)
    addProperties(vortex.segments, velocity_superfluid)
    
    
#ax.legend()
plt.show()