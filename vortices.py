#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
class Vortex(object):
    
    """
    Attributes:
        N: initial number of segments
        segments: dics with positions
        getIndex(): search through list for certain index
    """
    
    def __init__(self, positions):
        self.N = len(positions)
        self.segments = np.array([
                {'coords' : positions[i],
                 'forward' : i+1,
                 'backward' : i-1} 
                for i in range(self.N) 
                ])
        
    def __repr__(self):
        return 'Quantum Vortex object'
    
    def getIndex(self, position):
        if (position > 0):
            i=0
            while (self.segments[i]['forward'] < position):
                i+=1
            return i
        else: raise TypeError('Position should be positive integer')
    
        
    def getCoords(self, position):
        index = self.getIndex(position)
        return self.segments[index]['coords']

    def getAxisCoords(self, axis):
        return [self.segments[i]['coords'][axis] 
                for i  in range(self.N)
                ]
    
    def getForward(self, position):
        index = self.getIndex(position)
        return self.segments[index]['forward']
    
    def getBackward(self, position):
        index = self.getIndex(position)
        return self.segments[index]['backward']
    
    
            