#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 03:26:07 2017

@author: kubo
"""
import numpy as np

def calc_tests(segments):
        length, curv, prod = np.zeros(3)
        N = len(segments)

        for item in segments:
            if item['forward'] is not None:
                nextItem = segments[item['forward']]
                length += np.linalg.norm( item['coords'] - nextItem['coords'] )
                curv += item['curvature'] / N
                prod += np.linalg.norm( np.cross(item['tangent'], item['curvature']) ) / N
        return length, curv, prod

def calc_error(theor, real):
    return 100*np.abs(theor - real) / theor

lenReal, curvReal, prodReal = calc_tests(vortex.segments)

lenTheor = 2*np.pi*radius
lenErr = calc_error(lenTheor, lenReal)

curvTheor = 1/radius
curvErr = calc_error(curvTheor, curvReal)

prodTheor = 1/radius
prodErr = calc_error(prodTheor, prodReal)

print('Vortex length error: {}%'.format(round(lenErr, 3)) )
print('Curvature error : {}%'.format(round(curvError, 3)))
print('s x s product error: {}%'.format(round(prodErr, 3)))
