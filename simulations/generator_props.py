#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 17:28:51 2017

@author: kubo
"""
import constants as c
from vandermonde import calc_FDcoeffs

import numpy as np


kappa = c.quantum_vorticity
a = c.vortex_width
v_s = c.velocity_superfluid

def go_backward(segments, item):
        return segments[item['backward']]
    
def go_forward(segments, item):
        return segments[item['forward']]   

def calc_derivative(segments, item, order=1, radius=2):
        for n in range(radius):
            item = go_backward(segments, item)
        firstItem = item
        
        neighCoords = []
        thisItem = firstItem
        for i in range(2*radius+1):
            neighCoords.append( thisItem['coords'] )
            thisItem = go_forward(segments, thisItem)
            
        loc_index = radius
            
        dists = [ np.linalg.norm( neighCoords[loc_index] - neighCoords[n] ) 
                  for n in range(2*radius+1) 
                  if n != loc_index ]
        
        coeffs = calc_FDcoeffs(dists, order)
        
        derivative = coeffs.dot(neighCoords)
        return derivative
    
def calc_velocity_LIA(segments, item):
    r = 1 / np.linalg.norm(item['curvature'])
    beta = kappa * np.log(r/a) / (4*np.pi)
    v_lia = beta * np.cross(item['tangent'], item['curvature'])
    return v_lia
    
def calc_velocity_BSL(segments, item):
    v_biot = 0 #kappa / (4*np.pi) # * BIOT-savart integral
    return v_biot

def calc_velocity_full(segments, item, v_s):
    v_full = item['velocity_LIA'] + item['velocity_Biot'] + v_s
    return v_full

def add_properties(segments, v_s):
    for item in segments:
        if (item['backward'] and item['forward']) is not None:
            if (go_backward(segments, item)['backward'] and go_forward(segments, item)['forward']) is not None:
                # derivatives
                item['tangent'] = calc_derivative(segments, item)
                item['curvature'] = calc_derivative(segments, item, order=2)
                
                # normalization
                mt = np.linalg.norm(item['tangent'])
                item['tangent'] /= mt
                item['curvature'] /= mt**2
                
                # velocities
                item['velocity_LIA'] = calc_velocity_LIA(segments, item)
                item['velocity_Biot'] = calc_velocity_BSL(segments, item)
                item['velocity_total'] = calc_velocity_full(segments, item, v_s)
            else:
                item['tangent'] = None
                item['curvature'] = None
                item['velocity_LIA'] = None
            
        else:   
            item['tangent'] = None
            item['curvature'] = None
            item['velocity_LIA'] = None
            
    #return segments