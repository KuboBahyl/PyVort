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
from run import make_step, change_step
import tests

def plot_vortex(vortex, ax):
    ax.scatter(vortex.getAllAxisCoords(0),
               vortex.getAllAxisCoords(1),
               vortex.getAllAxisCoords(2),
               label='ring',
               color='blue')
    ax.set_xlabel('x[$\mu$m]')
    ax.set_ylabel('y[$\mu$m]')
    ax.set_zlabel('z[$\mu$m]')
    if cf.plot_segments_save:
        plt.savefig('screens/step_'+str(i)+'.png')

###########################
###   VORTEX CREATION   ###
###########################
def init():
    # Initial position
    print('Initialising vortex ring of radius: {}mm with {} segments...\n'.format(10*cf.radius, cf.num_segments))

    shape = {'center': cf.center,
             'radius': cf.radius,
             'direction': cf.direction}

    # Coords init
    coords = create_ring(shape, cf.num_segments)

    # Vortex init
    vortex = createVortex(shape, coords)
    return vortex

def main(evolute=True,
         static_quantity_name=None,
         dynamic_quantity_name=None
         ):

    # init and filling the missing segment properties
    vortex = init()
    update_segments(vortex)

    # setting up collectors
    dynamic_list = np.zeros(cf.iters)

    ##########################
    ###   TIME EVOLUTION   ###
    ##########################
    if evolute:
        print('Time evolution started...')

        if cf.plot_segments:
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            plt.title(cf.plot_segments_name)

        for epoch in tqdm(range(cf.iters)):

            # TIME-STEP UPDATE
            cf.dt = change_step(vortex, cf.dt, cf.max_shift)

            # REPORT
            if cf.log_info:
                if ((epoch+1)%round(cf.iters/cf.reports)==0):
                    print('STARTING STEP {} with dt={}...'.format(i, cf.dt))
                    tests.print_statistics(vortex)

            # VISUALISATION
            if cf.plot_segments:
                if ((epoch+1)%round(cf.iters/cf.graphs)==0):
                    plot_vortex(vortex, ax)


            # KILL SMALL RINGS
            if (vortex.N < 10):
                print("Vortex ring too small, deleting...")
                break

            # DO TIME STEP
            make_step(cf.method, vortex, cf.dt)

            # RE-CONNECT
            new_connections(vortex)

            # RE-SEGMENT
            new_segmentation(vortex, cf.min_seg_distance, cf.max_seg_distance)

            # UPDATE SEGMENT PROPS
            update_segments(vortex)

            # collecting dynamical quantity
            if dynamic_quantity_name is not None:
                if dynamic_quantity_name in vortex.__dict__.keys():
                    dynamic_list[epoch] = getattr(vortex, dynamic_quantity_name)
                elif dynamic_quantity_name in tests.__dict__.keys():
                     method = getattr(tests, dynamic_quantity_name)
                     dynamic_list[epoch] = method(vortex)

        if cf.plot_segments:
            plt.show()

    if static_quantity_name is not None:
        if static_quantity_name in vortex.__dict__.keys():
            return getattr(vortex, static_quantity_name)
        elif static_quantity_name in tests.__dict__.keys():
             method = getattr(tests, static_quantity_name)
             quantity = method(vortex)
             return quantity

    if dynamic_quantity_name is not None:
        return dynamic_list

if (__name__ == "__main__"):
    main()
