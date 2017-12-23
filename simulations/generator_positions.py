#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Here are prepared 3 types of vortex shape. Each of them should be defined
with following parameters and their ordering:

- STRAIGHT LINE: 
    shape='straight'
    number of segments (int)
    beginning point coords (list of length 3)
    ending point coords (list of length 3)
                 
- RING: 
    shape='ring'
    number of segments (int)
    ring center coords (list of length 3)
    ring radius (float)


- RANDOM: 
    shape='random'
    number of segments (int)
"""
import random
import numpy as np

def generate_positions(shape, N, *args):
    if (shape == 'straight'):
        begin, end = np.array(args[0]), np.array(args[1])
        step = (end - begin) / N
        positions = np.array([ i*step
                            for i in range(N+1)
                            ])
    
    if (shape == 'ring'):
        center, radius = np.array(args[0]), args[1]
        step = 2*np.pi/N
        positions = np.array([ center + [0, radius*np.sin(i*step), radius*np.cos(i*step)] 
                               for i in range (N)
                            ])
    
    if (shape == 'random'):
        positions = np.array([ [i, i**2, i+random.randint(-10,10)/100] 
                               for i in range(N)
                            ])
    
    return positions
    