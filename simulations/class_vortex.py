#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

class Vortex(object):
    
    """
    Attributes:
        N: initial number of segments
        segments: dicts with positions, list position, derivatives, velocities
    """
    
    def __init__(self, positions):
        self.N = len(positions)
        self.segments = np.array([
                {'coords' : positions[i],
                 'backward' : i-1,
                 'forward' : i+1} 
                for i in range(self.N) 
                ])
   
    def __repr__(self):
        return 'Quantum Vortex object. Check documentation for available methods.'

    def go_backward(self, item):
        return self.segments[item['backward']]
    
    def go_forward(self, item):
        return self.segments[item['forward']]     

    def get_index(self, position):
        if (position >= 0):
            if self.segments[position]['forward'] == position + 1:
                return position
            else:
                raise Exception('TODO searching in segments')
        else: raise TypeError('Position should be positive integer')
         
######################################
### CLEANING
######################################
    def normalization(self):
        for item in self.segments:
            item['tangent'] /= np.linalg.norm(item['tangent'])
            item['curvature'] /= np.linalg.norm(item['curvature'])
            
    def delete_small_loops(self):
        pass


######################################
### TESTING
######################################
        
    def fullLength(self):
        length = 0
        for item in self.segments:
            if item['forward'] is not None:  
                nextItem = self.segments[item['forward']]
                dist = np.linalg.norm( item['coords'] - nextItem['coords'] )
                length += dist
        return length
    
######################################
### USER'S OPTION
######################################                        
            
    def addSegment_Dumb(self, back, forw, coords):
        new_index = len(self.segments)
        self.segments = np.append(self.segments, 
                                  {'coords' : coords,
                                   'backward' : back,
                                   'forward' : forw})
        self.segments[back]['forward'] = new_index
        self.segments[forw]['backward'] = new_index
        
    def getCoords(self, position):
        index = self.get_index(position)
        return self.segments[index]['coords']

    def getAllAxisCoords(self, axis):
        return [self.segments[i]['coords'][axis] 
                for i  in range(self.N)]