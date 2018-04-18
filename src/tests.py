#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import constants as c
from config import Config as cf

kappa = 10**8*c.quantum_vorticity # to um^2/s
a_core = 10**4*c.core_width # to um

### Some of the tests are very specific for ring object
def calc_length_stat(Vortex, segdists=False):
    length = 0
    segmin = np.inf
    segmax = 0

    for item in Vortex.segments:
        if item['is_active']:
            nextItem = Vortex.segments[item['forward']]
            segdist = np.linalg.norm(item['coords'] - nextItem['coords'])
            segdist = np.linalg.norm(item['coords'] - nextItem['coords'])
            segmin = segdist if (segdist < segmin) else segmin
            segmax = segdist if (segdist > segmax) else segmax
            length += segdist

    if segdists:
        return length, segmin, segmax #cm

    return length

def calc_velocity_ring(Env, Ring, Vortex):
    radius = Ring.radius
    v_n = Env.vel_n
    v_s = Env.vel_s
    alpha1, alpha2 = c.get_mutual_coeffs(cf.temperature)
    ind = ["x", "y", "z"].index(Ring.direction)

    v_i = np.zeros(3)
    v_i[ind] =  kappa * (np.log(8*radius/a_core) - 1/2) / (4*np.pi*radius)
    v = (1 - alpha2) * (v_i + v_s) + alpha2*v_n
    v_len = np.linalg.norm(v)

    return v_len # um/s

def calc_energy_ring(Ring, Vortex):
    rho_tot, rho_s = c.get_densities(cf.temperature)
    rho_tot /= 10**18
    radius = Ring.radius
    E = kappa**2 * rho_tot * radius * (np.log(8*radius/a_core) - 2) / 2 # kg um^2 / s^2
    E_scalled = E / (10**12 * 1.6 * 1e-19) # ev
    return E_scalled

def calc_error(real, theor):
    return (real - theor) / theor

def kill_if_length_error(Ring, Vortex):
    length_real = calc_length_stat(Vortex)
    length_theor = 2 * np.pi * Ring.radius
    length_err = calc_error(length_real, length_theor)

    if (length_err < -cf.length_max_error):
        print("Small number of segments!")

    elif (length_err > cf.length_max_error):
        print("Segments are too noisy!")
        raise ValueError('Length error too high!')

def print_statistics(Env, Ring, Vortex):
    radius = Ring.radius
    length_real, segmin, segmax = calc_length_stat(Vortex, segdists=True)
    length_theor = 2 * np.pi * radius
    length_err = calc_error(length_real, length_theor)

    velocity_theor = calc_velocity_ring(Env, Ring, Vortex)

    energy = calc_energy_ring(Ring, Vortex)

    print('Number of segments: {}'.format(Vortex.active_segments))
    print('Resolution: {}um'.format(cf.resolution))
    print('Min and max segment distance: {}um, {}um'.format(round(segmin, 2), round(segmax, 2)))
    print('Center {}-shift: {}um'.format(Ring.direction, round(Ring.center,2)))
    print('Radius: {}um'.format(round(Ring.radius, 2)))
    print('Velocity {}-real: {}um/s'.format(Ring.direction, round(Ring.velocity, 2)))
    print('Velocity {}-theor: {}um/s'.format(Ring.direction, round(velocity_theor, 2)))
    print('Vortex length error: {}%'.format(round(100*length_err, 2)))
    print('Vortex energy: {}kev'.format(round(energy/10**3,3)))
    print('....................')

def print_graph(Vortex):
    for j in range(len(Vortex.segments)):
        seg = Vortex.segments[j]
        print("ind {}, back {}, forw {}".format(j, seg['backward'],seg['forward']))
