#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 17:28:51 2017

@author: kubo
"""
from scipy import interpolate
from spline3D import spline3D
import numpy as np
import math

from config import Config as cf
import constants as c
import finitediffs

kappa = c.quantum_vorticity
a = c.vortex_width

def go_backward(segments, item):
    return segments[item['backward']]

def go_forward(segments, item):
    return segments[item['forward']]

def delete_item(segments, itemindex_to_delete):
    segments = np.delete(segments, itemindex_to_delete)
    for item in segments:
        if (item['forward'] > itemindex_to_delete):
            item['forward'] -= 1
        if (item['backward'] > itemindex_to_delete):
            item['backward'] -= 1
    return segments

def calc_derivative(segments, item, order=1):
    # start with the first item in range
    firstItem = go_backward(segments, go_backward(segments, item))

    # extract coords from each item
    neighCoords = []
    thisItem = firstItem
    for i in range(5):
        neighCoords.append(thisItem['coords'])
        thisItem = go_forward(segments, thisItem)

    # calculate coeffs for numeric derivative
    try:
        coeffs = finitediffs.calc_FDcoeffs_inverse(neighCoords, order)
    except:
        coeffs = finitediffs.calc_FDcoeffs_closed(neighCoords, order)

    derivative = coeffs.dot(neighCoords)
    return derivative

def calc_velocity_LIA(vortex, item):
    if cf.BIOT:
        item_prev = go_backward(vortex.segments, item)
        item_next = go_forward(vortex.segments, item)
        len_prev = np.linalg.norm(item_prev['coords'] - item['coords'])
        len_next = np.linalg.norm(item_next['coords'] - item['coords'])

        log_term = 2 * np.sqrt(len_prev * len_next) / (a * np.e)
        beta = kappa * np.log(log_term) / (4*np.pi)
    else:
        r = 1 / np.linalg.norm(item['curvature'])
        beta = kappa * np.log(2*r/a) / (4*np.pi)

    v_lia = beta * np.cross(item['tangent'], item['curvature'])
    return v_lia

def calc_velocity_BIOT(vortex, item):
    segments = vortex.segments
    velocity_biot = np.zeros(3)

    for other_item in segments:
        next_item = go_forward(segments, other_item)
        if (other_item['forward'] != item['forward'] and next_item['forward'] != item['forward']):
            R_this = other_item['coords'] - item['coords']
            R_next = next_item['coords'] - item['coords']
            R_this_len = np.linalg.norm(R_this)
            R_next_len = np.linalg.norm(R_next)

            first_term = (R_this_len + R_next_len) / (R_this_len * R_next_len)
            second_term = np.cross(R_this, R_next) / (R_this_len * R_next_len + np.dot(R_this, R_next))

            velocity_biot += (kappa / 4*np.pi) * first_term * second_term

    return velocity_biot

def calc_velocity_drive(vortex, item):
    v_n = np.array(cf.velocity_normal_ext)
    v_s = np.array(cf.velocity_super_ext)

    v_ns = v_n - v_s
    v_i = item['velocity_LIA'] + item['velocity_BIOT']
    alpha1, alpha2 = c.get_mutual_coeffs(cf.temperature)

    v_drive1 = np.cross(item['tangent'], v_ns - v_i)
    v_drive2 = np.cross(item['tangent'], v_drive1)
    v_drive_full = alpha1*v_drive1 - alpha2*v_drive2
    return v_drive_full

def calc_velocity_full(vortex, item):
    v_s = np.array(cf.velocity_super_ext)
    v_full = v_s + item['velocity_LIA'] + item['velocity_BIOT'] + item['velocity_drive']
    return v_full

def update_segments(vortex):
    segments = vortex.segments
    ind = ["x", "y", "z"].index(vortex.shape['direction'])
    N = vortex.N
    vortex.velocity = 0

    for item in segments:
        # derivatives
        item['tangent'] = calc_derivative(segments, item, order=1)
        item['curvature'] = calc_derivative(segments, item, order=2)

        # normalisation
        norm = np.linalg.norm(item['tangent'])
        item['tangent'] /= norm
        item['curvature'] /= norm**2 # maybe not so useful

        # velocities
        item['velocity_LIA'] = calc_velocity_LIA(vortex, item)
        if cf.BIOT:
            item['velocity_BIOT'] = calc_velocity_BIOT(vortex, item)
        if cf.Quantum:
            item['velocity_drive'] = calc_velocity_drive(vortex, item)
        item['velocity_full'] = calc_velocity_full(vortex, item)
        vortex.velocity += item['velocity_full'][ind] / N

def update_vortex(vortex):
    center, radius, velocity, length = np.zeros(4)
    N = vortex.N
    ind = ["x", "y", "z"].index(vortex.shape['direction'])
    other = np.delete(np.array([0,1,2]), ind)

    segmin = np.inf
    segmax = 0

    for item in vortex.segments:
        center += item['coords'][ind] / N
        radius += np.sqrt(item['coords'][other[0]]**2 + item['coords'][other[1]]**2) / N

        nextItem = vortex.segments[item['forward']]
        segdist = np.linalg.norm(item['coords'] - nextItem['coords'])
        segmin = segdist if (segdist < segmin) else segmin
        segmax = segdist if (segdist > segmax) else segmax
        length += segdist

    vortex.shape['center'][ind] = center
    vortex.shape['radius'] = radius

    return center, radius, segmin, segmax, length

def new_connections(vortex):
    pass
    """
    N = len(segments)
    new_segments = segments
    segments = np.delete(segments, segments[0])

    for i in range(N-1):
        focus_item = new_segments[i]
        mindist = math.inf

        for item in segments:
            dist = np.linalg.norm(focus_item['coords'] - item['coords'])
            if (dist < mindist):
                mindist = dist
                new_segments[i]['forward'] = np.asscalar(np.argwhere(segments==item))
                new_segments[i+1] = item

        segments = np.delete(segments, new_segments[i]['forward'])


    return new_segments
    """

def new_segmentation(vortex, dmin, dmax):
# assumes that indices are already assigned
    segments = vortex.segments

    dmin /= 10**4
    dmax /= 10**4
    i = 0

    while (i < len(segments)):
        item = segments[i]
        next_item = go_forward(segments, item)
        dist = np.linalg.norm(item['coords'] - next_item['coords'])

        if (dist < dmin):
            #make local interpolation with line using 4 points
            new_point = spline3D(segments, item, next_item, "nearest")

            # add new segment and remove the close ones
            segments = np.append(segments, {'coords' :  new_point,
                                            'backward' : item['backward'],
                                            'forward' : next_item['forward']})

            # update indices of new neighbours
            newitem_index = len(segments) - 1
            go_backward(segments, item)['forward'] = newitem_index
            go_forward(segments, next_item)['backward'] = newitem_index

            # safely delete disconnected segments
            segments = delete_item(segments, item['forward'])
            segments = delete_item(segments, next_item['backward'])

            i-=1

        elif (dist > dmax):
            #make local interpolation with line using 4 points
            new_point = spline3D(segments, item, next_item, "every_second")

            # add new segment along the distant ones
            segments = np.append(segments, {'coords' : new_point,
                                            'backward' : next_item['backward'],
                                            'forward' : item['forward']})

            # update indices of new neighbours
            newitem_index = len(segments) - 1
            item['forward'] = newitem_index
            next_item['backward'] = newitem_index

        i += 1
    vortex.segments = segments

"""
GOALS:
    - leapfrogging - two circles orbiting each other
    - intersection of two circles: as Emil's simulation
"""
