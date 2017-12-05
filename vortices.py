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
    
        # add derivatives
        for i in range(2,self.N-2):
            self.segments[i]['tangent'] = self.add_derivative(i)
            self.segments[i]['curvature'] = self.add_derivative(i, order=2)
        
    def __repr__(self):
        return 'Quantum Vortex object. Check documentation for available methods.'
    
    def add_derivative(self, index, order=1, area=5):
        neighbourCoords = []
        loc_index = int((area-1)/2)
        for i in range(area):
            neigh_index = index - loc_index + i
            neighbourCoords.append(self.segments[neigh_index]['coords'])
        
        h = np.linalg.norm(neighbourCoords[loc_index-1] - neighbourCoords[loc_index])
        
        if (order == 2):
            ders = (- 1*neighbourCoords[loc_index-2] 
                    + 16*neighbourCoords[loc_index-1] 
                    - 30*neighbourCoords[loc_index+0]
                    + 16*neighbourCoords[loc_index+1]
                    - 1*neighbourCoords[loc_index+2] ) / (12*h)
            return ders
        
        else:        
            ders = (  1*neighbourCoords[loc_index-2] 
                    - 8*neighbourCoords[loc_index-1] 
                    + 0*neighbourCoords[loc_index+0]
                    + 8*neighbourCoords[loc_index+1]
                    - 1*neighbourCoords[loc_index+2] ) / (12*h)
            return ders
    
    def get_index(self, position):
        if (position > 0):
            return position-1
        else: raise TypeError('Position should be positive integer')
        
        
        
        
    def getCoords(self, position):
        index = self.get_index(position)
        return self.segments[index]['coords']

    def getAllAxisCoords(self, axis):
        return [self.segments[i]['coords'][axis] 
                for i  in range(self.N)
                ]
        
    
    
            