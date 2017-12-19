#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import constants
from vandermonde import calc_FDcoeffs

kappa = constants.quantum_vorticity
a = constants.vortex_width
v_s = constants.velocity_superfluid

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
    
    def calc_velocity_LIA(self, item):
        r = 1 / np.linalg.norm(item['curvature'])
        beta = kappa * np.log(r/a) / (4*np.pi)
        v_lia = beta * np.cross(item['tangent'], item['curvature'])
        return v_lia
    
    def calc_velocity_BSL(self, item):
        v_biot = kappa / (4*np.pi) # * BIOT-savart integral
        return v_biot
    
    def calc_velocity_full(self, item, v_s):
        v_full = item['velocity_LIA'] + item['velocity_Biot'] + v_s
        return v_full
    
######################################
### TIME STEP & UPDATE
######################################
    def addProperties(self):
        for item in self.segments:
            if (item['backward'] and item['forward']) is not None:
                if (self.go_backward(item)['backward'] and self.go_forward(item)['forward']) is not None:
                    item['tangent'] = self.calc_derivative(item)
                    item['curvature'] = self.calc_derivative(item, radius=2, order=2)
                    item['velocity_LIA'] = self.calc_velocity_LIA(item)
                    item['velocity_Biot'] = self.calc_velocity_BSL(item)
                    item['velocity'] = self.calc_velocity_full(item, v_s)
                else:
                    item['tangent'] = None
                    item['curvature'] = None
                    item['velocity_LIA'] = None
                
            else:   
                item['tangent'] = None
                item['curvature'] = None
                item['velocity_LIA'] = None    
    
    def update_coords(self, dt):
        for item in self.segments:
            item['coords'] += item['velocity'] * dt 
            
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