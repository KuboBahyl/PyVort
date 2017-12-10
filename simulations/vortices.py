#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from vandermonde import calc_FDcoeffs

class Vortex(object):
    
    """
    Attributes:
        N: initial number of segments
        segments: dics with positions, relative position, derivatives
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
        if (position > 0):
            if self.segments[position]['forward'] == position + 1:
                return position
            else:
                raise Exception('TODO searching in segments')
        else: raise TypeError('Position should be positive integer')
    
    def calc_derivative(self, item, order=1, radius=2):
        for n in range(radius):
            item = self.go_backward(item)
        firstItem = item
        
        neighCoords = []
        thisItem = firstItem
        for i in range(2*radius+1):
            neighCoords.append( thisItem['coords'] )
            thisItem = self.go_forward(thisItem)
            
        loc_index = radius
            
        dists = [ np.linalg.norm( neighCoords[loc_index] - neighCoords[n] ) 
                  for n in range(2*radius+1) 
                  if n != loc_index ]
        
        coeffs = calc_FDcoeffs(dists, order)
        
        derivative = coeffs.dot(neighCoords)
        return derivative
        
        
######################################
### USER'S OPTIONS
######################################
        
    def addDerivatives(self):
        for item in self.segments:
            item['tangent'] = self.calc_derivative(item)
            item['curvature'] = self.calc_derivative(item, order=2)
            
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