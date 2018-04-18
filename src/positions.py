#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
- RING props:
    number of segments (int)
    ring center coords (array of length 3)
    ring radius (float)
    direction, where should the vortex ring go (array of length 3)
"""
import numpy as np
from config import Config as cf

def create_coords(Ring, res):
    if cf.is_ring:
        center = Ring.center
        radius = Ring.radius
        direction = Ring.direction

        N = int(2*np.pi*radius / res)
        step = 2*np.pi/N

        if (direction == "x"):
            coords = np.array([ center + [0, -radius*np.sin(i*step), radius*np.cos(i*step)] for i in range (N) ])

        elif (direction == "y"):
            coords = np.array([ center + [radius*np.sin(i*step), 0, radius*np.cos(i*step)] for i in range (N) ])

        elif (direction == "z"):
            coords = np.array([ center + [-radius*np.sin(i*step), radius*np.cos(i*step), 0] for i in range (N) ])

        return coords
