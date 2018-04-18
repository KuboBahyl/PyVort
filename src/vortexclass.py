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


# environment class - external sources of flow
class create_Env:
    def __init__(self, velocity_n_ext, velocity_s_ext):
        self.vel_n = np.array(velocity_n_ext)
        self.vel_s = np.array(velocity_s_ext)

    def evolute():
        # function how should external sources change in time
        pass

# vortex ring class - init only when simulation is focused on vortex rings
class create_Ring:
    def __init__(self, center, radius, direction):
        self.center = np.array(center)
        self.radius = radius
        self.direction = direction
        self.velocity = 0

# tangle o object containing all segmnets
class create_Vortex(object):
    def __init__(self, coords):
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
        N = self.active_segments
        self.segments[0]['backward'] = N - 1
        self.segments[N-1]['forward'] = 0

    def __repr__(self):
        return 'Quantum Vortex object. Check documentation for available methods.'


######################################
### USER'S OPTIONS
######################################

    # get coords of all segments
    def getAllCoords(self, index):
        return [item['coords']
                for item in self.segments]

    # get particular axis' coords of all segments
    # allowed input: "x", "y" or "z"
    def getAxisCoords(self, axis):
        ind = ["x", "y", "z"].index(axis)
        return [item['coords'][ind]
                for item in self.segments
                if item['active'] == True]
