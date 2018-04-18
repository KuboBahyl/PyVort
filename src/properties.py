#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 17:28:51 2017

@author: kubo
"""
from scipy import interpolate
from spline3D import spline3D
import numpy as np

from config import Config as cf
import constants as c
import finitediffs

kappa = 10**8*c.quantum_vorticity # to um^2/s
a_core = 10**4*c.core_width # to um

def go_backward(segments, item):
    return segments[item['backward']]

def go_forward(segments, item):
    return segments[item['forward']]

def calc_derivative(segments, item, order=1, neighbours=4):
    # start with the first item in range
    firstItem = go_backward(segments, go_backward(segments, item))

    # extract coords from each item
    neighCoords = []
    thisItem = firstItem
    for i in range(5):
        neighCoords.append(thisItem['coords'])
        thisItem = go_forward(segments, thisItem)

    # calculate coeffs for numeric derivative
    if (neighbours==4):
        coeffs = finitediffs.calc_FDcoeffs_closed(neighCoords, order)
    elif (neighbours>4):
        try:
            coeffs = finitediffs.calc_FDcoeffs_inverse(neighCoords, order)
        except:
            coeffs = finitediffs.calc_FDcoeffs_approx(neighCoords, order)


    derivative = coeffs.dot(neighCoords)
    return derivative

def calc_velocity_LIA(Vortex, item):
    if cf.use_LIA_updated:
        radius = 1 / np.linalg.norm(item['curvature'])
        beta = kappa * np.log(2*radius/a_core) / (4*np.pi)

    else:
        item_prev = go_backward(Vortex.segments, item)
        item_next = go_forward(Vortex.segments, item)
        len_prev = np.linalg.norm(item_prev['coords'] - item['coords'])
        len_next = np.linalg.norm(item_next['coords'] - item['coords'])

        log_term = np.sqrt(len_prev * len_next) / a_core
        beta = kappa * np.log(log_term) / (4*np.pi)

    v_lia = beta * np.cross(item['tangent'], item['curvature'])
    return v_lia

def calc_velocity_BIOT(Vortex, item):
    segments = Vortex.segments
    velocity_biot = np.zeros(3)

    for first_item in segments:
        if first_item['is_active']:
            second_item = go_forward(segments, first_item)
            if second_item['is_active']:
                if (first_item['forward'] != item['forward'] and second_item['forward'] != item['forward']):
                    R_first = first_item['coords'] - item['coords']
                    R_second = second_item['coords'] - item['coords']
                    R_first_len = np.linalg.norm(R_first)
                    R_second_len = np.linalg.norm(R_second)

                    first_term = (R_first_len + R_second_len) / (R_first_len * R_second_len)
                    second_term = np.cross(R_first, R_second) / (R_first_len * R_second_len + np.dot(R_first, R_second))

                    velocity_biot += kappa * first_term * second_term / (4 * np.pi)

    return velocity_biot

def calc_velocity_drive(Env, Vortex, item):
    v_n = Env.vel_n
    v_s = Env.vel_s

    v_ns = v_n - v_s
    v_i = item['velocity_LIA'] + item['velocity_BIOT']
    alpha1, alpha2 = c.get_mutual_coeffs(cf.temperature)

    v_drive1 = np.cross(item['tangent'], v_ns - v_i)
    v_drive2 = np.cross(item['tangent'], v_drive1)
    v_drive_full = alpha1*v_drive1 - alpha2*v_drive2
    return v_drive_full

def calc_velocity_full(Env, Vortex, item):
    v_s = np.array(Env.vel_s)
    v_full = v_s + item['velocity_LIA'] + item['velocity_BIOT'] + item['velocity_drive']
    return v_full

def update_segments(Env, Ring, Vortex):
    segments = Vortex.segments
    ind = ["x", "y", "z"].index(Ring.direction)
    other = np.delete(np.array([0,1,2]), ind)
    N = Vortex.active_segments

    center, radius, velocity = np.zeros(3)

    for item in segments:
        if item['is_active']:
            # derivatives
            item['tangent'] = calc_derivative(segments, item, order=1)
            item['curvature'] = calc_derivative(segments, item, order=2)

            # normalisation
            norm = np.linalg.norm(item['tangent'])
            item['tangent'] /= norm
            item['curvature'] /= norm**2 # maybe not so useful

            # velocities
            item['velocity_LIA'] = calc_velocity_LIA(Vortex, item)
            if cf.use_BIOT:
                item['velocity_BIOT'] = calc_velocity_BIOT(Vortex, item)
            if not cf.is_temp_zero:
                item['velocity_drive'] = calc_velocity_drive(Env, Vortex, item)
            item['velocity_full'] = calc_velocity_full(Env, Vortex, item)

            center += item['coords'][ind] / N
            radius += np.sqrt(item['coords'][other[0]]**2 + item['coords'][other[1]]**2) / N
            velocity += item['velocity_full'][ind] / N

    Ring.center = center
    Ring.radius = radius
    Ring.velocity = velocity

def new_connections(Vortex):
    pass

def new_segmentation(Vortex, dmin, dmax):

# assumes that segments are already reconnected = indices are assigned
    segments = Vortex.segments
    N = Vortex.active_segments

    i = 0

    while (i < len(segments)):
        item = segments[i]

        if item['is_active']:
            next_item = go_forward(segments, item)
            dist = np.linalg.norm(item['coords'] - next_item['coords'])

            if (dist < dmin):
                # make local interpolation with line using 4 points
                item['coords'] = spline3D(segments, item, next_item, type="nearest")

                # update new neighbours
                item['forward'] = next_item['forward']
                next_next_item = go_forward(segments, next_item)
                next_next_item['backward'] = next_item['backward']

                # making next_item inactive
                next_item['is_active'] = False

                N -= 1

            elif (dist > dmax):
                # make local interpolation with line using 4 points
                new_point = spline3D(segments, item, next_item, type="every_second")

                # add new segment along the distant ones
                segments = np.append(segments, {'is_active': True,
                                                'coords' : new_point,
                                                'backward' : next_item['backward'],
                                                'forward' : item['forward'],
                                                'velocity_LIA': np.zeros(3),
                                                'velocity_BIOT': np.zeros(3),
                                                'velocity_drive' : np.zeros(3),
                                                'velocity_full' : np.zeros(3)
                                                })

                # update indices of new neighbours
                newitem_index = len(segments) - 1
                item['forward'] = newitem_index
                next_item['backward'] = newitem_index

                N += 1

        i += 1

    # making sure of boundaries
    #N = len(segments)
    #segments[0]['backward'] = N - 1
    #segments[N-1]['forward'] = 0

    # Vortex updates
    Vortex.segments = segments
    Vortex.active_segments = N
