#!/usr/bin/env python3
"""
Here is performed the main loop of simulation.
"""
###################
###   IMPORTS   ###
###################

# Numerics, plots
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from tqdm import tqdm

# Dependencies
from config import Config as cf
from positions import create_coords
from vortexclass import create_Env, create_Ring, create_Vortex
from run import make_step, change_step
import tests

def plot_vortex(Vortex, ax):
    ax.scatter(Vortex.getAxisCoords("x"),
               Vortex.getAxisCoords("y"),
               Vortex.getAxisCoords("z"),
               label='ring',
               color='blue')
    ax.set_xlabel('x[$\mu$m]')
    ax.set_ylabel('y[$\mu$m]')
    ax.set_zlabel('z[$\mu$m]')
    if cf.plot_segments_save:
        plt.savefig('graphics/'+cf.plot_segments_filename+'.pdf')

### THIS WILL BE REMOVED
########################################################################
def get_static_prop(Vortex, static_quantity_name):
    if static_quantity_name in Vortex.__dict__.keys():
        return getattr(Vortex, static_quantity_name)
    elif static_quantity_name in tests.__dict__.keys():
         method = getattr(tests, static_quantity_name)
         quantity = method(Vortex)
         return quantity
    else:
        raise ValueError("Given prop '{}' not found".format(static_quantity_name))
########################################################################


###########################
###   Vortex CREATION   ###
###########################
def init():
    # Initial position
    print('Initialising Vortex ring of radius: {}um with segment resolution {}um...\n'.format(cf.radius, cf.resolution))

    Env = create_Env(cf.velocity_normal_ext, cf.velocity_super_ext)

    # Ring object init and coords creation
    if cf.is_ring:
        Ring = create_Ring(cf.center, cf.radius, cf.direction)
        coords = create_coords(Ring, cf.resolution)

    # Vortex init
    Vortex = create_Vortex(coords)
    return Env, Ring, Vortex

def main(evolute=True,
         static_quantity_name=None,
         dynamic_quantity_name=None,
         dynamic_quantity_name2=None,
         ):

    # init and filling the missing segment properties
    Env, Ring, Vortex = init()
    Vortex.update_segments(Env, Ring)

    # setting up collectors
    dynamic_list = np.zeros(cf.epochs)
    dynamic_list2 = np.zeros(cf.epochs)

    ##########################
    ###   TIME EVOLUTION   ###
    ##########################
    if evolute:
        print('Time evolution started...')

        if cf.plot_segments:
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            plt.title(cf.plot_segments_title)

        for epoch in tqdm(range(cf.epochs)):

            ### THIS WILL BE REMOVED
            ########################################################################
            # collecting dynamical quantities
            if dynamic_quantity_name is not None:
                if dynamic_quantity_name in Vortex.__dict__.keys():
                    dynamic_list[epoch] = getattr(Vortex, dynamic_quantity_name)
                elif dynamic_quantity_name in Ring.__dict__.keys():
                    dynamic_list[epoch] = getattr(Ring, dynamic_quantity_name)
                elif dynamic_quantity_name in tests.__dict__.keys():
                     method = getattr(tests, dynamic_quantity_name)
                     dynamic_list[epoch] = method(Vortex)

            if dynamic_quantity_name2 is not None:
                if dynamic_quantity_name2 in Vortex.__dict__.keys():
                    dynamic_list2[epoch] = getattr(Vortex, dynamic_quantity_name2)
                elif dynamic_quantity_name2 in Ring.__dict__.keys():
                    dynamic_list[epoch] = getattr(Ring, dynamic_quantity_name2)
                elif dynamic_quantity_name2 in tests.__dict__.keys():
                     method = getattr(tests, dynamic_quantity_name2)
                     dynamic_list2[epoch] = method(Vortex)
            ########################################################################

            # REPORT
            if cf.log_info:
                if ((epoch+1)%round(cf.epochs/cf.log_num)==0):
                    print('STARTING STEP {} with dt={}...'.format(epoch, cf.dt))
                    tests.print_statistics(Env, Ring, Vortex)

            # VISUALISATION
            if cf.plot_segments:
                if ((epoch+1)%round(cf.epochs/cf.plot_num)==0):
                    plot_vortex(Vortex, ax)

            # KILL SMALL RINGS
            if (Vortex.active_segments < cf.min_num_seg):
                print("Vortex ring too small, deleting...")
                break

            # TIME-STEP UPDATE
            cf.dt = change_step(Ring, cf.dt, cf.max_shift)

            # DO TIME STEP
            make_step(Env, Ring, Vortex, cf.dt, cf.method)

            # RE-CONNECT
            Vortex.update_connections()

            # RE-SEGMENT
            Vortex.update_segmentation(min_dist=cf.min_seg_distance,
                                       max_dist=cf.max_seg_distance)

            # KILL IF TOO BIG CIRCUMFERENCE ERROR
            tests.kill_if_length_error(Ring, Vortex)

            # UPDATE SEGMENT PROPS
            Vortex.update_segments(Env, Ring)

        if cf.plot_segments:
            plt.show()

    ### THIS WILL BE REMOVED
    ########################################################################
    if static_quantity_name is not None:
        if static_quantity_name=="epoch":
            return cf.epochs
        quanity = get_static_prop(Vortex, static_quantity_name)
        return quanity

    if dynamic_quantity_name is not None:
        return dynamic_list, dynamic_list2
    ########################################################################

if (__name__ == "__main__"):
    main()
