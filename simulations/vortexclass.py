#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vortex class content:
    - constructor: assigns initial positions and relative position (neigbours) to each segment
    - method to focus on backward neighbour
    - method to focus on forward neighbour
    - method to add another segment anywhere
    - method to gain info about certain segment's coords
    - method to gain all coords along certain direction (0=x,1=y,2=z)

"""

import numpy as np

class Vortex(object):

    """
    Constructor attributes:
        N: initial number of segments
        segments: list of dicts with 3D coordinates
    """

    # basic neighbour init
    def __init__(self, coords):
        self.N = len(coords)
        self.segments = np.array([
                {'coords' : coords[i],
                 'backward' : i-1,
                 'forward' : i+1,
                 'tangent' : None,
                 'curvature' : None,
                 'velocity_LIA' : None,
                 'velocity_drive' : None,
                 'velocity_line' : None}
                for i in range(self.N)
                ])

    def __repr__(self):
        return 'Quantum Vortex object. Check documentation for available methods.'

    def go_backward(self, item):
        return self.segments[item['backward']]

    def go_forward(self, item):
        return self.segments[item['forward']]

######################################
### USER'S OPTIONS
######################################

    def addSegment_Dumb(self, back, forw, coords):
        new_index = len(self.segments)
        self.segments = np.append(self.segments,
                                  {'coords' : coords,
                                   'backward' : back,
                                   'forward' : forw})
        self.segments[back]['forward'] = new_index
        self.segments[forw]['backward'] = new_index

    def getAllCoords(self, index):
        return [self.segments[i]['coords']
                for i in range(self.N)]

    def getAllAxisCoords(self, axis):
        return [self.segments[i]['coords'][axis]
                for i  in range(self.N)]

"""
Maybe it will be useful later

    def get_index(self, position):
        if (position >= 0):
            if self.segments[position]['forward'] == position + 1:
                return position
            else:
                raise Exception('TODO searching in segments')
        else: raise TypeError('Position should be positive integer')
"""
