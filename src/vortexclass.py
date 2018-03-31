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
    def __init__(self, shape, coords, env):
        self.shape = shape
        self.velocity = 0
        self.N = len(coords)
        self.segments = np.array([
                {'coords' : coords[i],
                 'backward' : i-1,
                 'forward' : i+1,
                 'tangent' : None,
                 'curvature' : None,
                 'velocity_LIA' : None,
                 'velocity_BIOT': None,
                 'velocity_drive' : None,
                 'velocity_full' : None}
                 for i in range(self.N)
                ])
        self.env = env # static

    def __repr__(self):
        return 'Quantum Vortex object. Check documentation for available methods.'


######################################
### USER'S OPTIONS
######################################

    def getAllCoords(self, index):
        return [self.segments[i]['coords']
                for i in range(len(self.segments))]

    def getAllAxisCoords(self, axis):
        return [10**4*self.segments[i]['coords'][axis]
                for i  in range(len(self.segments))]

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
