#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

# solving M*coeffs = b

def calc_FDcoeffs(h, order):

    Taylor = np.array([ [1,1,1,1,1],
                        [-1,-1,0,1,1],
                        [1/2,1/2,0,1/2,1/2],
                        [-1/6,-1/6,0,1/6,1/6],
                        [1/24,1/24,0,1/24,1/24] ])
    
    Vandermond = np.array([ [1,1,1,1,1],
                            [h[0],h[1],0,h[2],h[3]],
                            [h[0]**2,h[1]**2,0,h[2]**2,h[3]**2],
                            [h[0]**3,h[1]**3,0,h[2]**3,h[3]**3],
                            [h[0]**4,h[1]**4,0,h[2]**4,h[3]**4] ])
    
    M = np.multiply(Taylor, Vandermond)
    
    b = np.zeros(5)
    b[order] = 1
    
    #np.set_printoptions(suppress=True)
    coeffs = np.linalg.pinv(M).dot(b)
    return coeffs

