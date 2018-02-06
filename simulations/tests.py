#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 03:26:07 2017

@author: kubo
"""
import numpy as np

def calc_testprops(segments):
        length, curv, prod, centerX = np.zeros(4)
        N = len(segments)

        dmin = 1000
        dmax = 0

        for item in segments:
            if item['forward'] is not None:
                centerX += item['coords'][0] / N
                nextItem = segments[item['forward']]
                dist = np.linalg.norm(item['coords'] - nextItem['coords'])
                if (dist < dmin):
                    dmin = dist
                if (dist > dmax):
                    dmax = dist
                length += dist
                curv += np.linalg.norm(item['curvature']) / N
                prod += np.linalg.norm(np.cross(item['tangent'], item['curvature'])) / N
        return 10000*dmin, 10000*dmax, 10*centerX, length, curv, prod

def calc_error(theor, real):
    return 100*(real - theor) / theor

def do_statistics(vortex, radius):

    dmin, dmax, centerX, lenReal, curvReal, prodReal = calc_testprops(vortex.segments)

    lenTheor = 2*np.pi*radius
    lenErr = calc_error(lenTheor, lenReal)

    curvTheor = 1/radius
    curvErr = calc_error(curvTheor, curvReal)

    prodTheor = 1/radius
    prodErr = calc_error(prodTheor, prodReal)

    print('Number of segments: {}'.format(len(vortex.segments)))
    print('Minimal and maximal distance: {}um, {}um'.format(round(dmin, 2), round(dmax, 2)))
    print('Center x-shift: {}mm'.format(round(centerX,2)))
    print('Vortex length error: {}%'.format(round(lenErr, 2)))
    print('Curvature |s\'\'| error : {}%'.format(round(curvErr, 2)))
    print('|s\' x s\'\'| product error: {}%'.format(round(prodErr, 2)))
