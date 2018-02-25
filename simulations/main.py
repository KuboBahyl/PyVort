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
#import os
#os.chdir('/home/kubo/MEGAsync/Github/superfluid/simulations')
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
print('Initializing vortex of radius 1mm...')

# Initial position
shape = 'ring'
pieces = 100
center = [0,0,0]
radius = 0.1 #cm = 1000um
print('Ring of radius: {}cm and segment length: {}um'.format(radius, round(10**4 * 2*np.pi*radius/pieces, 2)))
print('....................................')

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
iters = 3
dt=1e-2

min_distance=0 #um
max_distance=62.8 #um
max_shift = 2 #um

velocities_real = []
velocities_theor = []

fig = plt.figure()
ax = fig.gca(projection='3d')

# other parameters
graphs = 3
reports = 3

for i in range(iters):

    if (i%round(iters/reports)==0):
        print('STARTING STEP {} with dt={}...'.format(i, dt))

        # Testing parameters
        vel_real, vel_theor = showStat(vortex, radius)
        velocities_real.append(vel_real)
        velocities_theor.append(vel_theor)


    if (i%round(iters/graphs)==0):
        # Plotting
        ax.scatter(vortex.getAllAxisCoords(0),
                   vortex.getAllAxisCoords(1),
                   vortex.getAllAxisCoords(2),
                   label='ring',
                   color='blue')

    # Time evolution
    makeStep(vortex, dt, method="rk4")
    velocity = np.absolute(vortex.segments[0]['velocity_line'][0])
    #if (10000*velocity*dt > max_shift):
    #    dt *= 1/2 
    updateConnections(vortex)
    updateSegmentation(vortex, min_distance, max_distance)
    #min_distance = len(vortex.segments) / 2
    updateVelocities(vortex)


plt.title('Ring motion')
#plt.savefig('euler-50-instability.pdf')
#plt.show()

# Velicity evolution
plt.figure()
plt.scatter([i*round(iters/reports) for i in range(reports)], velocities_real,
             label="Simulation")
plt.scatter([i*round(iters/reports) for i in range(reports)], velocities_theor,
             label="Theory")
plt.legend(loc=2)
plt.title('Velocity evolution')

#%%
