#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

# solving M*coeffs = b
# Finite difference coefficients using 2 neighbours on each side

def calc_FDcoeffs_inverse(coords, order, radius):
    center = radius
    l1, l2, l3, l4 = [np.linalg.norm(coords[n] - coords[center])
                          for n in range(2*radius+1)
                          if n != center]
    Taylor = np.array([ [1,1,1,1,1],
                        [-1,-1,0,1,1],
                        [1/2,1/2,0,1/2,1/2],
                        [-1/6,-1/6,0,1/6,1/6],
                        [1/24,1/24,0,1/24,1/24] ])

    Vandermond = np.array([ [1,1,1,1,1],
                            [l1**1, l2**1, 0, l3**1, l4**1],
                            [l1**2, l2**2, 0, l3**2, l4**2],
                            [l1**3, l2**3, 0, l3**3, l4**3],
                            [l1**4, l2**4, 0, l3**4, l4**4]
                            ])

    M = np.multiply(Taylor, Vandermond)

    b = np.zeros(5)
    b[order] = 1

    #np.set_printoptions(suppress=True)
    coeffs = np.linalg.pinv(M).dot(b)
    return coeffs

def calc_FDcoeffs_closed(coords, order, radius):
    l1, l2, l3, l4 = [np.linalg.norm(coords[n] - coords[n+1])
                  for n in range(2*radius)]

    if (order == 1):
        A = (l2*l3**2 + l2*l3*l4) / (l1*(l1+l2) * (l1+l2+l3) * (l1+l2+l3+l4))
        B = (-l1*l3**2 - l2*l3**2 - l1*l3*l4 - l2*l3*l4) / (l1 * l2 * (l2+l3) * (l2+l3+l4))
        D = (l1*l2*l3 + l2**2*l3 + l1*l2*l4 + l2**2*l4) / (l3 * l4 * (l2+l3) * (l1+l2+l3))
        E = (-l3*l2**2 - l1*l2*l3) / (l4 * (l3+l4) * (l2+l3+l4) * (l1+l2+l3+l4))
        C = -(A+B+D+E)

    if (order == 2):
        A = 2*(-2*l2*l3 + l3**2 - l2*l4 + l3*l4) / (l1 * (l1+l2) * (l1+l2+l3) * (l1+l2+l3+l4))
        B = 2*(2*l1*l3 + 2*l2*l3 - l3**2 + l1*l4 + l2*l4 - l3*l4) / (l1 * l2 * (l2+l3) * (l2+l3+l4))
        D = 2*(-l1*l2 - l2**2 + l1*l3 + 2*l2*l3 + l1*l4 + 2*l2*l4) / (l3 * l4 * (l2+l3) * (l1+l2+l3))
        E = 2*(l1*l2 + l2**2 - l1*l3 - 2*l2*l3) / (l4 * (l3+l4) * (l2+l3+l4) * (l1+l2+l3+l4))
        C = -(A+B+D+E)

    return np.array([A,B,C,D,E])
