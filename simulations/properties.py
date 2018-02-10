#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 17:28:51 2017

@author: kubo
"""
import constants as c
import numpy as np
import math

import vandermonde

rho = c.density_total
rho_s = c.density_superfluid
v_n = c.velocity_normal
v_s = c.velocity_superfluid

kappa = c.quantum_vorticity
a = c.vortex_width

alpha1 = c.alpha1_mutual
alpha2 = c.alpha2_mutual

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

def calc_derivative(segments, item, order=1, radius=2):
    # start with the first item in range
    for n in range(radius):
        item = go_backward(segments, item)
    firstItem = item

    # extract coords from each item
    neighCoords = []
    thisItem = firstItem
    for i in range(2*radius+1):
        neighCoords.append(thisItem['coords'])
        thisItem = go_forward(segments, thisItem)

    # calculate coeffs for numeric derivative
    try:
        coeffs = vandermonde.calc_FDcoeffs_invert(neighCoords, order, radius)
    except:
        coeffs = vandermonde.calc_FDcoeffs_closed(neighCoords, order, radius)

    derivative = coeffs.dot(neighCoords)
    return derivative

def calc_velocity_LIA(item):
    r = 1 / np.linalg.norm(item['curvature'])
    beta = kappa * np.log(r/a) / (4*np.pi)
    v_lia = beta * np.cross(item['tangent'], item['curvature'])
    return v_lia

def calc_velocity_drive(item):
    v_ns = v_n - v_s
    v_lia = item['velocity_LIA']

    v_drive1 = np.cross(item['tangent'], v_ns - v_lia)
    v_drive2 = np.cross(item['tangent'], v_drive1)
    v_drive_full = alpha1*v_drive1 - alpha2*v_drive2
    return v_drive_full

def calc_velocity_full(item):
    v_full = item['velocity_LIA'] + v_s + item['velocity_drive']
    return v_full

def add_properties(vortex):
    segments = vortex.segments
    for item in segments:
        if (item['backward'] and item['forward']) is not None:
            if (go_backward(segments, item)['backward'] and go_forward(segments, item)['forward']) is not None:

                # derivatives
                item['tangent'] = calc_derivative(segments, item)
                item['curvature'] = calc_derivative(segments, item, order=2)

                # normalisation
                norm = np.linalg.norm(item['tangent'])
                item['tangent'] /= norm
                item['curvature'] /= norm**2 # maybe not so useful

                # velocities
                item['velocity_LIA'] = calc_velocity_LIA(item)
                item['velocity_drive'] = calc_velocity_drive(item)
                item['velocity_line'] = calc_velocity_full(item)

# TODO new everything
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
        firstItem = segments[i]
        nextItem = go_forward(segments, firstItem)
        dist = np.linalg.norm(firstItem['coords'] - nextItem['coords'])

        if (dist < dmin):
            # add new segment and remove the close ones
            segments = np.append(segments, {'coords' : (firstItem['coords'] + nextItem['coords']) / 2,
                                            'backward' : firstItem['backward'],
                                            'forward' : nextItem['forward']})

            # update indices of new neighbours
            newitem_index = len(segments) - 1
            go_backward(segments, firstItem)['forward'] = newitem_index
            go_forward(segments, nextItem)['backward'] = newitem_index

            # safely delete disconnected segments
            segments = delete_item(segments, firstItem['forward'])
            segments = delete_item(segments, nextItem['backward'])

            i-=1

        elif (dist > dmax): #TODO local fit approx instead of new point in the middle
            segments = np.append(segments, {'coords' : (firstItem['coords'] + nextItem['coords']) / 2,
                                            'backward' : nextItem['backward'],
                                            'forward' : firstItem['forward']})
            newitem_index = len(segments) - 1
            firstItem['forward'] = newitem_index
            nextItem['backward'] = newitem_index

        i += 1
    vortex.segments = segments

"""
GOALS:
    - leapfrogging - two circles orbiting each other
    - intersection of two circles: as Emil's simulation
"""
