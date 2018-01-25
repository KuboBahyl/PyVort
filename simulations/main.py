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
import vortexclass
import steps
import properties

# Basic operations init
def createPositions(shape, pieces, *args):
    return positions.generate_positions(shape, pieces, *args)

def createVortex(positions):
    return vortexclass.Vortex(positions)

def eulerStep(vortex, dt):
    return steps.euler_step(vortex, dt)

def rk4Step(vortex, dt):
    return steps.rk4_step(vortex, dt)

def updateProperties(segments):
    return properties.add_properties(segments)

#%%

##################################
###   SINGLE VORTEX CREATION
##################################
print('Initializing vortex...')

# Initial position
shape = 'ring'
pieces = 100
center = [0,0,0]
radius = 0.1 #cm = 1 mm

coords = createPositions(shape, pieces, center, radius)

# Vortex init
vortex = createVortex(coords)

# Fixing boundary neighbours
vortex.segments[0]['backward'] = pieces - 1
vortex.segments[pieces-1]['forward'] = 0

# Adding properties - s', s'', velocities
updateProperties(vortex.segments)

#%%

##########################
###   TIME EVOLUTION   ###
##########################
print('Time evolution started...')

# Time steps and steplength
iters = 501
dt=1e-2

#mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')

for i in range(iters):

    if (i%50==0):
        print('Starting step {}:'.format(i))

    # Testing parameters
        exec(compile(open('tests.py').read(), 'tests.py', 'exec'))

    # Plotting
        ax.plot(vortex.getAllAxisCoords(0),
               vortex.getAllAxisCoords(1),
               vortex.getAllAxisCoords(2),
               label='ring',
               color='blue')

    # Time evolution
    rk4Step(vortex, dt)

#ax.legend()
#plt.title('Ring instability with Euler step')
#plt.savefig('euler-50-instability.pdf')
plt.show()
