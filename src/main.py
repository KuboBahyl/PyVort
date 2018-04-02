#!/usr/bin/env python3
"""
Here is performed the main loop of simulation.
To clear all data, execute `%reset` in ipython console
"""
###################################################
###   IMPORTS   ###
###################

# Numerics, plots
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from tqdm import tqdm

# Dependencies
from config import Config as cf
from positions import create_ring
from vortexclass import Vortex as createVortex
from properties import new_segmentation, new_connections, update_segments
from tests import calc_velocity_ring, print_statistics
from run import make_step, change_step

###########################
###   VORTEX CREATION   ###
###########################

# Initial position
print('Initialising vortex ring of radius: {}mm and inter-segment distance: {}um...\n'.format(10*cf.radius, round(10**4 * 2*np.pi*cf.radius/cf.num_segments, 2)))

shape = {'center': cf.center,
         'radius': cf.radius,
         'direction': cf.direction}

# Coords init
coords = create_ring(shape, cf.num_segments)

# Vortex init
vortex = createVortex(shape, coords)

# Filling segment properties - tangent, curvature, velocities
update_segments(vortex)

##########################
###   TIME EVOLUTION   ###
##########################

print('Time evolution started...')

steps = []
velocities_real = []
velocities_theor = []

if cf.plot_segments:
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    plt.title(cf.plot_segments_name)

for i in tqdm(range(cf.iters)):

    # change dt
    cf.dt = change_step(vortex, cf.dt, cf.max_shift)

    # REPORT
    if ((i+1)%round(cf.iters/cf.reports)==0):
        print('STARTING STEP {} with dt={}...'.format(i, cf.dt))
        print_statistics(vortex)

        velocity_real = vortex.velocity
        velocity_theory = calc_velocity_ring(vortex)

        steps.append(i)
        velocities_real.append(velocity_real)
        velocities_theor.append(velocity_theory)

    # VISUALISATION
    if cf.plot_segments:
        if ((i+1)%round(cf.iters/cf.graphs)==0):
            ax.scatter(vortex.getAllAxisCoords(0),
                    vortex.getAllAxisCoords(1),
                    vortex.getAllAxisCoords(2),
                    label='ring')
                    #color='blue')
            ax.set_xlabel('x[$\mu$m]')
            ax.set_ylabel('y[$\mu$m]')
            ax.set_zlabel('z[$\mu$m]')
            if cf.plot_segments_save:
                plt.savefig('screens/step_'+str(i)+'.png')

    # KILL SMALL RINGS
    if (len(vortex.segments) < 10):
        print("Vortex ring too small, deleting...")
        break

    # TIME EVOLUTION
    make_step(cf.method, vortex, cf.dt)

    # new connections
    new_connections(vortex) # TODO

    # new segments
    new_segmentation(vortex, cf.min_seg_distance, cf.max_seg_distance)
    vortex.N = len(vortex.segments)

    #min_seg_distance = vortex.N / 2
    update_segments(vortex)

if cf.plot_segments:
    plt.show()

# Velocity evolution
if cf.plot_velocities:
    plt.figure()
    plt.scatter(steps, velocities_real, label="Simulation")
    plt.scatter(steps, velocities_theor, label="Theory")
    plt.legend(loc=2)
    plt.title(cf.plot_velocities_name)
    plt.show()
    if cf.plot_segments_save:
        plt.savefig('screens/velocities.png')
