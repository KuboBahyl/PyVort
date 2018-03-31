#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 03:26:07 2017

@author: kubo
"""
import numpy as np
import constants as c
from properties import update_vortex

kappa = 100 * c.quantum_vorticity # to mm^2/s
a = 10 * c.vortex_width # to mm

### Some of the tests are very specific for ring object

def calc_velocity_ring(vortex):
    radius = vortex.shape['radius']
    return kappa / (4*np.pi*radius) * (np.log(8*radius/a) - 1) # in um/s

def calc_error(theor, real):
    return 100*(real - theor) / theor

def print_statistics(vortex):
    center, radius, velocity, segmin, segmax, length = update_vortex(vortex)

    velocity_theor = calc_velocity_ring(vortex)

    length_theor = 2*np.pi*radius
    lenErr = calc_error(length_theor, length)

    print('Number of segments: {}'.format(vortex.N))
    print('Min and max segment distance: {}um, {}um'.format(round(10**4*segmin, 2), round(10**4*segmax, 2)))
    print('Center {}-shift: {}mm'.format(vortex.shape['direction'], round(10*center,2)))
    print('Radius: {}mm'.format(round(10*radius, 2)))
    print('Velocity {}-real: {}mm/s'.format(vortex.shape['direction'], round(10**velocity, 2)))
    print('Velocity {}-theor: {}mm/s'.format(vortex.shape['direction'], round(10**velocity_theor, 2)))
    print('Vortex length error: {}%'.format(round(lenErr, 2)))
    print('....................')

def test_indices(vortex):
    for j in range(len(vortex.segments)):
        seg = segments[j]
        print("ind {}, back {}, forw {}".format(j, seg['backward'],seg['forward']))
