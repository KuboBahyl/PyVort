#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 17:28:51 2017

@author: kubo
"""
import constants as c
from vandermonde import calc_FDcoeffs

import numpy as np
import math

kappa = c.quantum_vorticity
a = c.vortex_width
v_s = c.velocity_superfluid
rho = c.density_total
rho_s = c.density_superfluid
alpha1 = c.alpha1_mutual
alpha2 = c.alpha2_mutual

def go_backward(segments, item):
        return segments[item['backward']]

def go_forward(segments, item):
        return segments[item['forward']]

def calc_derivative(segments, item, order=1, radius=2):
        for n in range(radius):
            item = go_backward(segments, item)
        firstItem = item

        neighCoords = []
        thisItem = firstItem
        for i in range(2*radius+1):
            neighCoords.append( thisItem['coords'] )
            thisItem = go_forward(segments, thisItem)

        loc_index = radius

        dists = [ np.linalg.norm( neighCoords[loc_index] - neighCoords[n] )
                  for n in range(2*radius+1)
                  if n != loc_index ]

        coeffs = calc_FDcoeffs(dists, order)

        derivative = coeffs.dot(neighCoords)
        return derivative

def calc_velocity_LIA(segments, item):
    r = 1 / np.linalg.norm(item['curvature'])
    beta = kappa * np.log(r/a) / (4*np.pi)
    v_lia = beta * np.cross(item['tangent'], item['curvature'])
    return v_lia

def calc_velocity_drive(segments, item):
    v_tot = item['velocity_LIA'] + v_s

    v_drive = alpha1*np.cross(item['tangent'], v_tot) + alpha2*v_tot
    return v_drive

def calc_velocity_full(segments, item):
    v_full = item['velocity_LIA'] + v_s + item['velocity_drive']
    return v_full

def add_properties(segments):
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
                item['velocity_LIA'] = calc_velocity_LIA(segments, item)
                item['velocity_drive'] = calc_velocity_drive(segments, item)
                item['velocity_line'] = calc_velocity_full(segments, item)

def new_connection(segments):
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



def new_segmentation(segments):
# assumes that indices are already assigned
    dmin = 0
    dmax = 100
    for item in segments:
        nextItem = segments[item['forward']]
        dist = np.linalg.norm(item['coords'] - nextItem['coords'])
        if (dist < dmin):
            segments = np.append(segments, {'coords' : (item['coords'] + nextItem['coords']) / 2,
                                            'backward' : item['backward'],
                                            'forward' : nextItem['forward']})
            new_index = len(segments)
            segments[item['backward']]['forward'] = new_index
            segments[nextItem['forward']]['backward'] = new_index
            segments = np.delete(segments, [item, nextItem])

        elif (dist > dmax):
            segments = np.append(segments, {'coords' : (item['coords'] + nextItem['coords']) / 2,
                                            'backward' : nextItem['backward'],
                                            'forward' : item['forward']})
            new_index = len(segments)
            item['forward'] = new_index
            nextItem['backward'] = new_index
