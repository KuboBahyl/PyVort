#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 18:32:55 2017

@author: kubo
"""
import numpy as np
import copy as cp
import properties

def updateVelocities(vortex):
    return properties.add_properties(vortex)

###############################################################

def euler_step(vortex, dt):
    segments = vortex.segments
    for item in segments:
        item['coords'] += item['velocity_line'] * dt

def rk4_step(vortex, dt):
    # making vortex copy
    virtualVortex = cp.deepcopy(vortex)

    # real and virtual segments
    real_seg = vortex.segments
    virtual_seg = virtualVortex.segments
    N = len(real_seg)

    # RK4 coefficients
    k1, k2, k3, k4 = [np.zeros([N,3]) for i in range(4)]

    for i in range(N):
        k1[i] = real_seg[i]['velocity_line']
        virtual_seg[i]['coords'] = real_seg[i]['coords'] + k1[i] * dt * 0.5

    updateVelocities(virtualVortex)

    for i in range(N):
        k2[i] = virtual_seg[i]['velocity_line']
        virtual_seg[i]['coords'] = real_seg[i]['coords'] + k2[i] * dt * 0.5

    updateVelocities(virtualVortex)

    for i in range(N):
        k3[i] = virtual_seg[i]['velocity_line']
        virtual_seg[i]['coords'] = real_seg[i]['coords'] + k3[i] * dt

    updateVelocities(virtualVortex)

    for i in range(N):
        k4[i] = virtual_seg[i]['velocity_line']
        real_seg[i]['coords'] += (1/6) * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) * dt
