#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Here is performed the main loop of simulation.
To clear all data, execute `%reset` in ipython console
"""
#%%
###################
###   IMPORTS
###################

# Libraries
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# Objects, functions
import positions
import steps

from vortexclass import Vortex as createVortex
from properties import new_segmentation as updateSegmentation
from properties import new_connections as updateConnections
from properties import add_properties as updateVelocities
from tests import do_statistics as showStat

# Basic operations init
def createPositions(shape, pieces, *args):
    if (shape == 'line'):
        return positions.create_line(shape, pieces, *args)
    elif (shape == 'ring'):
        return positions.create_ring(shape, pieces, *args)
    elif (shape == 'random'):
        return positions.create_random(shape, pieces, *args)

def makeStep(vortex, dt, method):
    if method=="euler":
        return steps.euler_step(vortex, dt)
    elif method=="rk4":
        return steps.rk4_step(vortex, dt)

#%%

##################################
###   SINGLE VORTEX CREATION
##################################
print('Initializing vortex...')

# Initial position
shape = 'ring'
pieces = 100
center = [0,0,0]
radius = 0.1 #cm = 1000um
print('Ring of radius: {}cm and segment length: {}um'.format(radius, round(10**4 * 2*np.pi*radius/pieces, 2)))

coords = createPositions(shape, pieces, center, radius)

# Vortex init
vortex = createVortex(coords)

# Fixing boundary neighbours
vortex.segments[0]['backward'] = pieces - 1
vortex.segments[pieces-1]['forward'] = 0

# Adding properties - tangent, curvature => velocities
updateVelocities(vortex)

#%%

##########################
###   TIME EVOLUTION   ###
##########################
print('Time evolution started...')

# Time steps and steplength
iters = 101
dt=3e-2

min_distance=25
max_distance=100

#mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')

for i in range(iters):

    if (i%10==0):
        print('Starting step {}:'.format(i))

        # Testing parameters
        showStat(vortex, radius)

        # Plotting
        ax.plot(vortex.getAllAxisCoords(0),
               vortex.getAllAxisCoords(1),
               vortex.getAllAxisCoords(2),
               label='ring',
               color='blue')

    # Time evolution
    makeStep(vortex, dt, method="rk4")
    updateConnections(vortex)
    updateSegmentation(vortex, min_distance, max_distance)
    updateVelocities(vortex)


#ax.legend()
#plt.title('Ring instability with Euler step')
#plt.savefig('euler-50-instability.pdf')
plt.show()
