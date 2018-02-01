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

def makeStep(vortex, dt, method):
    if method=="euler":
        return steps.euler_step(vortex, dt)
    elif method=="rk4":
        return steps.rk4_step(vortex, dt)

def updateSegmentation(vortex, min_distance, max_distance):
    return properties.new_segmentation(vortex, min_distance, max_distance)

def updateConnections(vortex):
    return properties.new_connections(vortex)

def updateVelocities(vortex):
    return properties.add_properties(vortex)



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
dt=1e-3

#mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')

for i in range(iters):

    if (i%10==0):
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
    makeStep(vortex, dt=1e-3, method="rk4")
    updateConnections(vortex)
    updateSegmentation(vortex, min_distance=25, max_distance=100)
    updateVelocities(vortex)


#ax.legend()
#plt.title('Ring instability with Euler step')
#plt.savefig('euler-50-instability.pdf')
plt.show()
