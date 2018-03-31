#!/usr/bin/env python3
"""
Here is performed the main loop of simulation.
To clear all data, execute `%reset` in ipython console
"""
#####################################################
# Physics
temperature = 1.5 # K
center = [0,0,0]
radius = 0.1 #cm = 1000um
direction = "z"

# Simulation parameters
segments = 100
iters = 5
dt=1e-2
method = "euler"

# Hyper-parametes
min_seg_distance=50 #um
max_seg_distance=100 #um

# Output parameters
max_plot_shift = 2 #um
graphs = 5
reports = 1

#####################################################

###################
###   IMPORTS
###################

# Numerics, plots
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# Dependencies
import constants as c
from positions import create_ring
from vortexclass import Vortex as createVortex
from properties import new_segmentation as updateSegmentation
from properties import new_connections as updateConnections
from properties import update_velocities
from tests import do_statistics as showStat
from run import make_step

##################################
###   VORTEX CREATION
##################################

# Initial position
print('Initialising vortex ring of radius: {}mm and inter-segment distance: {}um...\n'.format(10*radius, round(10**4 * 2*np.pi*radius/segments, 2)))

coords = create_ring(segments, center, radius, direction)

# Vortex init
vortex = createVortex(coords)

# Fixing boundary neighbours
vortex.segments[0]['backward'] = segments - 1
vortex.segments[segments-1]['forward'] = 0

# Adding properties - tangent, curvature => velocities
update_velocities(vortex)

##########################
###   TIME EVOLUTION   ###
##########################
print('Time evolution started...')

velocities_real = []
velocities_theor = []

fig = plt.figure()
ax = fig.gca(projection='3d')
plt.title('Ring motion')

for i in range(iters):

    if ((i+1)%round(iters/reports)==0):
        print('STARTING STEP {} with dt={}...'.format(i, dt))

        # Testing parameters
        vel_real, vel_theor = showStat(vortex, radius)
        velocities_real.append(vel_real)
        velocities_theor.append(vel_theor)


    if ((i+1)%round(iters/graphs)==0):
        # Plotting

        ax.scatter(vortex.getAllAxisCoords(0),
                   vortex.getAllAxisCoords(1),
                   vortex.getAllAxisCoords(2),
                   label='ring')#,
                   #color='blue')

        plt.savefig('screens/step_'+str(i)+'.png')
    # Check if ring is not too small
    if (len(vortex.segments) < 10):
        print("Vortex ring too small, deleting...")
        break

    # Time evolution
    make_step(method, vortex, dt)

    velocity = np.absolute(vortex.segments[0]['velocity_line'][0])
    if (10000*velocity*dt > max_plot_shift):
        dt *= 1/2
    updateConnections(vortex)
    updateSegmentation(vortex, min_seg_distance, max_seg_distance)
    min_distance = len(vortex.segments) / 2

    update_velocities(vortex)

plt.show()
# Velicity evolution
plt.figure()
plt.scatter([i*round(iters/reports) for i in range(reports)], velocities_real,
             label="Simulation")
plt.scatter([i*round(iters/reports) for i in range(reports)], velocities_theor,
             label="Theory")
plt.legend(loc=2)
plt.title('Velocity evolution')
