#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import constants as c
from config import Config as cf

kappa = c.quantum_vorticity # to um^2/s
a = c.vortex_width # to mm

### Some of the tests are very specific for ring object
def calc_length_res(vortex, segdists=False):
    length = 0
    segmin = np.inf
    segmax = 0

    for item in vortex.segments:
        if item['active']:
            nextItem = vortex.segments[item['forward']]
            segdist = np.linalg.norm(item['coords'] - nextItem['coords'])
            segdist = np.linalg.norm(item['coords'] - nextItem['coords'])
            segmin = segdist if (segdist < segmin) else segmin
            segmax = segdist if (segdist > segmax) else segmax
            length += segdist

    if segdists:
        return length, segmin, segmax #cm

    return length

def calc_velocity_ring(vortex):
    radius = vortex.shape['radius']
    return kappa * (np.log(8*radius/a) - 1) / (4*np.pi*radius) # cm/s

def calc_energy_ring(vortex):
    rho_tot, rho_s = c.get_densities(cf.temperature)
    radius = vortex.shape['radius']
    E = kappa**2 * rho_tot * radius * (np.log(8*radius/a) - 2) / 2 # g cm / s^2
    E_scalled = E / (1000 * 100 * 1.6 * 1e-19) # ev
    return E_scalled

def calc_error(real, theor):
    return (real - theor) / theor

def print_statistics(vortex):
    radius = vortex.shape['radius']
    length_real, segmin, segmax = calc_length_res(vortex, segdists=True)

    length_theor = 2*np.pi*radius
    length_err = calc_error(length_real, length_theor)

    velocity = vortex.velocity
    velocity_theor = calc_velocity_ring(vortex)

    energy = calc_energy_ring(vortex)

    print('Number of segments: {}'.format(vortex.active_segments))
    print('Resolution: {}um'.format(cf.resolution))
    print('Min and max segment distance: {}um, {}um'.format(round(10**4*segmin, 2), round(10**4*segmax, 2)))
    print('Center {}-shift: {}um'.format(vortex.shape['direction'], round(10**4*vortex.shape['center'],2)))
    print('Radius: {}mm'.format(round(10*radius, 2)))
    print('Velocity {}-real: {}um/s'.format(vortex.shape['direction'], round(10**4*velocity, 2)))
    print('Velocity {}-theor: {}um/s'.format(vortex.shape['direction'], round(10**4*velocity_theor, 2)))
    print('Vortex length error: {}%'.format(round(100*length_err, 2)))
    print('Vortex energy: {}Mev'.format(round(energy/10**6,3)))
    print('....................')

def print_graph(vortex):
    for j in range(len(vortex.segments)):
        seg = vortex.segments[j]
        print("ind {}, back {}, forw {}".format(j, seg['backward'],seg['forward']))
