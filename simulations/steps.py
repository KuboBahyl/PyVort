#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 18:32:55 2017

@author: kubo
"""
import numpy as np
import copy as cp
import vortexclass
import properties

def createVortex(positions):
    return vortexclass.Vortex(positions)

def updateProperties(segments):
    return properties.add_properties(segments)

###############################################################

def euler_step(vortex, dt):
    segments = vortex.segments
    for item in segments:
        item['coords'] += item['velocity_line'] * dt

    updateProperties(segments)

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

    updateProperties(virtual_seg)

    for i in range(N):
        k2[i] = virtual_seg[i]['velocity_line']
        virtual_seg[i]['coords'] = real_seg[i]['coords'] + k2[i] * dt * 0.5

    updateProperties(virtual_seg)

    for i in range(N):
        k3[i] = virtual_seg[i]['velocity_line']
        virtual_seg[i]['coords'] = real_seg[i]['coords'] + k3[i] * dt

    updateProperties(virtual_seg)

    for i in range(N):
        k4[i] = virtual_seg[i]['velocity_line']
        real_seg[i]['coords'] += (1/6) * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) * dt

    updateProperties(real_seg)
