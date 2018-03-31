#!/usr/bin/env python3
"""
Here is performed the main loop of simulation.
To clear all data, execute `%reset` in ipython console
"""
######################
### USER'S OPTIONS ###
###################################################

# Environment parameters
temperature = 1.5 # K
velocity_normal_ext = [0,0,0]
velocity_super_ext = [0,0,0]

# Vortex ring parameters
center = [0,0,0]
radius = 0.1 #cm = 1000um
direction = "x"

# Simulation parameters
num_segments = 100
iters = 10
dt=1e-2
method = "RK4"

# Hyper-parametes
min_seg_distance=50 #um
max_seg_distance=100 #um

# Output parameters
max_plot_shift = 5 #um
graphs = 10
reports = 10

###################################################
###   IMPORTS   ###
###################

# Numerics, plots
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# Dependencies
import constants as c
from positions import create_ring
from vortexclass import Vortex as createVortex
from properties import new_segmentation
from properties import new_connections
from properties import update_segments
from tests import calc_velocity_ring, print_statistics
from run import make_step

###########################
###   VORTEX CREATION   ###
###########################

# Initial position
print('Initialising vortex ring of radius: {}mm and inter-segment distance: {}um...\n'.format(10*radius, round(10**4 * 2*np.pi*radius/num_segments, 2)))

shape = {'center': center,
         'radius': radius,
         'direction': direction}

env = {'temperature': temperature,
       'velocity_normal': velocity_normal_ext,
       'velocity_super': velocity_super_ext}

# Coords init
coords = create_ring(shape, num_segments)
# Vortex init
vortex = createVortex(shape, coords, env)
# Fixing boundary neighbours
vortex.segments[0]['backward'] = num_segments - 1
vortex.segments[num_segments-1]['forward'] = 0
# Filling segment properties - tangent, curvature, velocities
update_segments(vortex)

##########################
###   TIME EVOLUTION   ###
##########################

print('Time evolution started...')

steps = []
velocities_real = []
velocities_theor = []

fig = plt.figure()
ax = fig.gca(projection='3d')
plt.title('Ring motion')

for i in range(iters):

    # change dt
    if (10000*vortex.velocity*dt > max_plot_shift):
        dt *= 1/2

    # REPORT
    if ((i+1)%round(iters/reports)==0):
        print('STARTING STEP {} with dt={}...'.format(i, dt))


        print_statistics(vortex)

        velocity_real = vortex.velocity
        velocity_theory = calc_velocity_ring(vortex)

        steps.append(i)
        velocities_real.append(velocity_real)
        velocities_theor.append(velocity_theory)

    # VISUALISATION
    if ((i+1)%round(iters/graphs)==0):
        ax.scatter(vortex.getAllAxisCoords(0),
                   vortex.getAllAxisCoords(1),
                   vortex.getAllAxisCoords(2),
                   label='ring')#,
                   #color='blue')
        ax.set_xlabel('x[$\mu$m]')
        ax.set_ylabel('y[$\mu$m]')
        ax.set_zlabel('z[$\mu$m]')
        #plt.savefig('screens/step_'+str(i)+'.png')

    # KILL SMALL RINGS
    if (len(vortex.segments) < 10):
        print("Vortex ring too small, deleting...")
        break

    # TIME EVOLUTION
    make_step(method, vortex, dt)

    # new connections
    new_connections(vortex) # TODO

    # new segments
    new_segmentation(vortex, min_seg_distance, max_seg_distance)
    vortex.N = len(vortex.segments)

    #min_seg_distance = vortex.N / 2
    update_segments(vortex)

plt.show()

# Velocity evolution
plt.figure()
plt.scatter(steps, velocities_real, label="Simulation")
plt.scatter(steps, velocities_theor, label="Theory")
plt.legend(loc=2)
plt.title('Velocity evolution')
#plt.show()
