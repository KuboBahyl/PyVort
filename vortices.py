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
    
    def calc_derivative(self, item, order=1, dist=2):
        neighCoords = []
        firstItem = self.go_backward(self.go_backward(item))
        thisItem = firstItem
        for i in range(2*dist+1):
            neighCoords.append( thisItem['coords'] )
            thisItem = self.go_forward(thisItem)
            
        loc_index = dist
        h = np.linalg.norm(neighCoords[loc_index-1] - neighCoords[loc_index])
        
        if (order == 2):
            ders = (- 1*neighCoords[loc_index-2] 
                    + 16*neighCoords[loc_index-1] 
                    - 30*neighCoords[loc_index+0]
                    + 16*neighCoords[loc_index+1]
                    - 1*neighCoords[loc_index+2] ) / (12*h)
            return ders
        
        else:        
            ders = (  1*neighCoords[loc_index-2] 
                    - 8*neighCoords[loc_index-1] 
                    + 0*neighCoords[loc_index+0]
                    + 8*neighCoords[loc_index+1]
                    - 1*neighCoords[loc_index+2] ) / (12*h)
            return ders
    
    def get_index(self, position):
        if (position > 0):
            if self.segments[position]['forward'] == position + 1:
                return position
            else:
                raise Exception('TODO searching in segments')
        else: raise TypeError('Position should be positive integer')
        
######################################
### USER'S OPTIONS
######################################
    def addDerivatives(self):
        for item in self.segments:
            item['tangent'] = self.calc_derivative(item)
            item['curvature'] = self.calc_derivative(item, order=2)
        
    def getCoords(self, position):
        index = self.get_index(position)
        return self.segments[index]['coords']

    def getAllAxisCoords(self, axis):
        return [self.segments[i]['coords'][axis] 
                for i  in range(self.N)
                ]
        
    
    
            