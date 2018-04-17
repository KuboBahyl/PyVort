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
        plt.savefig('graphics/'+cf.plot_segments_filename+'.pdf')

def get_static_prop(vortex, static_quantity_name):
    if static_quantity_name in vortex.__dict__.keys():
        return getattr(vortex, static_quantity_name)
    elif static_quantity_name in tests.__dict__.keys():
         method = getattr(tests, static_quantity_name)
         quantity = method(vortex)
         return quantity
    else:
        raise ValueError("Given prop '{}' not found".format(static_quantity_name))


###########################
###   VORTEX CREATION   ###
###########################
def init():
    # Initial position
    print('Initialising vortex ring of radius: {}mm with resulution {}um...\n'.format(cf.radius/10**3, cf.resolution))

    shape = {'center': cf.center,
             'radius': cf.radius/10**4, # to cm
             'direction': cf.direction}

    # Coords init
    coords = create_ring(shape, cf.resolution/10**4)

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
    dynamic_list = np.zeros(cf.epochs)

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

            # collecting dynamical quantity
            if dynamic_quantity_name is not None:
                if dynamic_quantity_name in vortex.__dict__.keys():
                    dynamic_list[epoch] = getattr(vortex, dynamic_quantity_name)
                elif dynamic_quantity_name in tests.__dict__.keys():
                     method = getattr(tests, dynamic_quantity_name)
                     dynamic_list[epoch] = method(vortex)

            # TIME-STEP UPDATE
            cf.dt = change_step(vortex, cf.dt, cf.max_shift)

            # REPORT
            if cf.log_info:
                if ((epoch+1)%round(cf.epochs/cf.log_num)==0):
                    print('STARTING STEP {} with dt={}...'.format(epoch, cf.dt))
                    tests.print_statistics(vortex)

            # VISUALISATION
            if cf.plot_segments:
                if ((epoch+1)%round(cf.epochs/cf.plot_num)==0):
                    plot_vortex(vortex, ax)


            # KILL SMALL RINGS
            if (vortex.active_segments < cf.min_num_seg):
                print("Vortex ring too small, deleting...")
                break

            # DO TIME STEP
            make_step(cf.method, vortex, cf.dt)

            # RE-CONNECT
            new_connections(vortex)

            # RE-SEGMENT
            new_segmentation(vortex, cf.min_seg_distance, cf.max_seg_distance)

            # KILL IF TOO BIG CIRCUMFERENCE ERROR
            length_real = tests.calc_length_res(vortex)
            length_theor = 2*np.pi*vortex.shape['radius']
            length_err = tests.calc_error(length_real, length_theor)
            if (length_err < -cf.length_max_error):
                print("Small number of segments!")
                if (static_quantity_name=="epoch"):
                    return epoch

            elif (length_err > cf.length_max_error):
                print("Segments are too noisy!")
                if (static_quantity_name=="epoch"):
                    return epoch
                raise ValueError('Length error too high!')


            # UPDATE SEGMENT PROPS
            update_segments(vortex)

        if cf.plot_segments:
            plt.show()

    if static_quantity_name is not None:
        if static_quantity_name=="epoch":
            return cf.epochs
        quanity = get_static_prop(vortex, static_quantity_name)
        return quanity

    if dynamic_quantity_name is not None:
        return dynamic_list

if (__name__ == "__main__"):
    main()
