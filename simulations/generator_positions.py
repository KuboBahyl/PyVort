#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Straight line inputs: number of segments, positions of begin and enf of line
Ring inputs: number of segments, center position, radius
random inputs: number of segments
"""
import random
import numpy as np

def generate_positions(shape, *args):
    N = args[0]
    if (shape == 'straight'):
        begin, end = np.array(args[1]), np.array(args[2])
        step = (end - begin) / N
        positions = np.array([ step*i
                            for i in range(N+1)
                            ])
    
    if (shape == 'ring'):
        center, radius = np.array(args[1]), args[2]
        step = 2*np.pi/N
        positions = np.array([ center + [0, radius*np.sin(i*step), radius*np.cos(i*step)] 
                               for i in range (N)
                            ])
    
    if (shape == 'random'):
        positions = np.array([ [i, i**2, i+random.randint(-10,10)/100] 
                               for i in range(N)
                            ])
    
    return positions
    