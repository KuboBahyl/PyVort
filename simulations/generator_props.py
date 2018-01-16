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
rho = c.density_total

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
    
def calc_velocity_drive(segments, item):
    B1, B2, rho_n = np.zeros(3)
    
    alpha1 = rho_n*B1 / (2*rho)
    alpha2 = rho_n*B2 / (2*rho)
    v_tot = item['velocity_LIA'] + v_s
    
    v_drive = alpha1*np.cross(item['tangent'], v_tot) + alpha2*v_tot
    return v_drive

def calc_velocity_full(segments, item):
    v_full = item['velocity_LIA'] + v_s + item['velocity_drive'] 
    return v_full

def add_properties(segments):
    for item in segments:
        if (item['backward'] and item['forward']) is not None:
            if (go_backward(segments, item)['backward'] and go_forward(segments, item)['forward']) is not None:
                
                # derivatives
                item['tangent'] = calc_derivative(segments, item)
                item['curvature'] = calc_derivative(segments, item, order=2)
                
                # normalisation
                norm = np.linalg.norm(item['tangent'])
                item['tangent'] /= norm
                item['curvature'] /= norm**2
                
                # velocities
                item['velocity_LIA'] = calc_velocity_LIA(segments, item)
                item['velocity_drive'] = calc_velocity_drive(segments, item)
                item['velocity_line'] = calc_velocity_full(segments, item)
            else:
                item['tangent'] = None
                item['curvature'] = None
                item['velocity_LIA'] = None
            
        else:   
            item['tangent'] = None
            item['curvature'] = None
            item['velocity_LIA'] = None
            
    #return segments