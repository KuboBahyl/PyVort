#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
class Vortex(object):
    
    """
    Attributes:
        temp: temperature of system
        N: initial number of segments
        segments: dics with positions
    """
    
    def __init__(self, positions):
        self.N = len(positions)
        self.segments = np.array([
                {'position' : positions[i],
                 'forward' : i+1,
                 'backward' : i-1} 
                for i in range(self.N) 
                ])
        
    def __repr__(self):
        return 'Quantum Vortex object'
    
        
    def getPosition(self, index):
        return self.segments[index]['position']

    def getCoords(self, axis):
        return [self.segments[i]['position'][axis] for i  in range(self.N)]
            