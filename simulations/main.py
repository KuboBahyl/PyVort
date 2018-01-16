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
import generator_positions
import class_vortex
import stepping
import generator_props
from tests import fullLength

# Basic operations init
def createPositions(shape, pieces, *args):
    return generator_positions.generate_positions(shape, pieces, *args)

def createVortex(positions):
    return class_vortex.Vortex(positions)

def eulerStep(vortex, dt):
    return stepping.euler_step(vortex, dt)

def rk4Step(vortex, dt):
    return stepping.rk4_step(vortex, dt)

def updateProperties(segments):
    return generator_props.add_properties(segments)

#%%

##################################
###   SINGLE VORTEX CREATION
##################################

# Initial position
shape = 'ring'
pieces = 100
center = [0,0,0]
radius = 1e-5

positions = createPositions(shape, pieces, center, radius)

# Vortex init
vortex = createVortex(positions)

# Fixing boundary neighbours
vortex.segments[0]['backward'] = pieces - 1
vortex.segments[pieces-1]['forward'] = 0

# Adding properties - s', s'', velocities
updateProperties(vortex.segments)

#%%

##########################
###   TIME EVOLUTION   ###
##########################

# Time steps and steplength
steps = 2
dt=0.00001

#mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')

for i in range(steps):

    # Plotting
    #if (i%10==0):

    # Testing parameters
    print('Starting step {}:'.format(i))
    lengthTheor = 2*np.pi*radius
    lengthReal = fullLength(vortex.segments)
    lengthError = 100*np.abs(lengthReal - lengthTheor) / lengthTheor

    curvTheor = 1/radius
    curvReal = np.linalg.norm(vortex.segments[0]['curvature'])
    curvError = 100*np.abs(curvReal - curvTheor) / curvTheor

    print('Vortex length error: {}%'.format(round(lengthError, 3)) )
    print('Curvature error : {}%'.format(round(curvError, 3)))

    # Plotting
    ax.scatter(vortex.getAllAxisCoords(0),
           vortex.getAllAxisCoords(1),
           vortex.getAllAxisCoords(2),
           label='ring')

    # Time evolution
    rk4Step(vortex, dt)

#ax.legend()
plt.title('Ring instability')
#plt.savefig('ring-instability.pdf')
plt.show()
