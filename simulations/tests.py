#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 03:26:07 2017

@author: kubo
"""
import numpy as np
import constants as c

kappa = 100 * c.quantum_vorticity
a = 10 * c.vortex_width

### Some of the tests are very specific for ring object

def calc_testprops(segments):
        distX, radius, length, centerX, velocityX = np.zeros(5)
        N = len(segments)

        segmin = np.inf
        segmax = 0

        for item in segments:
            if item['forward'] is not None:
                distX += item['coords'][0] / N
                radius += np.sqrt(item['coords'][1]**2 + item['coords'][2]**2) / N
                velocityX += item['velocity_line'][0] / N

                nextItem = segments[item['forward']]
                segdist = np.linalg.norm(item['coords'] - nextItem['coords'])
                segmin = segdist if (segdist < segmin) else segmin
                segmax = segdist if (segdist > segmax) else segmax
                length += segdist

        return 10*distX, 10*radius, 10000*velocityX, 10000*segmin, 10000*segmax, length

def calc_error(theor, real):
    return 100*(real - theor) / theor

def do_statistics(vortex, radius):
    distX, radReal, velX, segmin, segmax, lenReal = calc_testprops(vortex.segments)

    radErr = calc_error(10*radius, radReal)

    velTheor = 1000 * kappa / (4*np.pi*radReal) * (np.log(8*radReal/a) - 1/2) # in um/s
    #velErr = calc_error(velTheor, velX)

    lenTheor = 2*np.pi*radius
    lenErr = calc_error(lenTheor, lenReal)

    print('Number of segments: {}'.format(len(vortex.segments)))
    print('Min and max segment distance: {}um, {}um'.format(round(segmin, 2), round(segmax, 2)))
    print('Radius: {}mm, decreased by: {}%'.format(round(radReal, 2), round(radErr, 2)))
    print('Center x-shift: {}mm'.format(round(distX,2)))
    print('Velocity x: {}um/s'.format(round(velX, 2)))
    print('Velocity x theor: -{}um/s'.format(round(velTheor, 2)))
    print('Vortex length error: {}%'.format(round(lenErr, 2)))
    print('....................')

    return np.absolute(velX), velTheor

def test_indices(segments):
    for j in range(len(segments)):
        seg = segments[j]
        print("ind {}, back {}, forw {}".format(j, seg['backward'],seg['forward']))
