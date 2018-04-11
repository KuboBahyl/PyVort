#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vortex class content:
    - constructor: assigns initial positions, relative position (neigbours) to each segment

    Methods:
    - get certain segment's coords
    - get all coords along certain direction {x,y,z}

"""

import numpy as np

class Vortex(object):

    def __init__(self, shape, coords):
        self.shape = shape # TODO refactor
        self.velocity = 0
        self.active_segments = len(coords)
        self.segments = np.array([
                {'active' : True,
                 'coords' : coords[i],
                 'backward' : i-1,
                 'forward' : i+1,
                 'tangent' : None,
                 'curvature' : None,
                 'velocity_LIA' : np.zeros(3),
                 'velocity_BIOT': np.zeros(3),
                 'velocity_drive' : np.zeros(3),
                 'velocity_full' : np.zeros(3)}
                 for i in range(self.active_segments)
                ])

        # boundary conditions for ring
        self.segments[0]['backward'] = self.active_segments - 1
        self.segments[self.active_segments-1]['forward'] = 0

    def __repr__(self):
        return 'Quantum Vortex object. Check documentation for available methods.'


######################################
### USER'S OPTIONS
######################################

    def getAllCoords(self, index):
        return [item['coords']
                for item in self.segments]

    def getAllAxisCoords(self, axis):
        return [10**4*item['coords'][axis]
                for item in self.segments
                if item['active'] == True]

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
