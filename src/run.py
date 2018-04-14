#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 18:32:55 2017

@author: kubo
"""
import numpy as np
import copy as cp
from properties import update_segments

def change_step(vortex, dt, max_shift):
    max_shift /= 10**4
    next_step = vortex.velocity * dt
    if (next_step > max_shift):
        dt = max_shift / vortex.velocity
        return dt

    return dt

def make_step(method, vortex, dt):
    if method=="euler":
        return euler_step(vortex, dt)
    elif method=="RK4":
        return rk4_step(vortex, dt)
    else:
        raise ValueError('Error in method definition. Use "euler" or "RK4" method')

###############################################################

def euler_step(vortex, dt):
    for item in vortex.segments:
        item['coords'] += item['velocity_full'] * dt

def rk4_step(vortex, dt):
    # making vortex copy
    virtualVortex = cp.deepcopy(vortex)

    # real and virtual segments
    segments_real = vortex.segments
    segments_virtual = virtualVortex.segments

    N = len(segments_real)

    # RK4 coefficients
    k1, k2, k3, k4 = [np.zeros([N,3]) for i in range(4)]

    for i in range(N):
        item_real = segments_real[i]
        if item_real['active']:
            item_virtual = segments_virtual[i]
            k1[i] = item_real['velocity_full']
            item_virtual['coords'] = item_real['coords'] + k1[i] * dt * 0.5

    update_segments(virtualVortex)

    for i in range(N):
        item_real = segments_real[i]
        if item_real['active']:
            item_virtual = segments_virtual[i]
            k2[i] = item_virtual['velocity_full']
            item_virtual['coords'] = item_real['coords'] + k2[i] * dt * 0.5

    update_segments(virtualVortex)

    for i in range(N):
        item_real = segments_real[i]
        if item_real['active']:
            item_virtual = segments_virtual[i]
            k3[i] = item_virtual['velocity_full']
            item_virtual['coords'] = item_real['coords'] + k3[i] * dt

    update_segments(virtualVortex)

    for i in range(N):
        item_real = segments_real[i]
        if item_real['active']:
            item_virtual = segments_virtual[i]
            k4[i] = item_virtual['velocity_full']
            item_real['coords'] += (1/6) * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) * dt
