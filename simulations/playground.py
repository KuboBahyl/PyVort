#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 09:35:46 2017

@author: kubo
"""

from vortices import Vortex

import numpy as np

"""
testPositions = np.array([[x, x**2, 0] for x in range(10)])
N = len(testPositions)

# init
testVortex = Vortex(testPositions)

# fixing neighbours for testline
testVortex.segments[0]['backward'] = None
testVortex.segments[N-1]['forward'] = None

# tests
testVortex.addProperties()
print(testVortex.segments)
"""
segments = np.random.rand(10)
N = len(segments)
new_segments = np.array(N)
new_segments[0] = segments[0]
segments = np.delete(segments, segments[0])

for i in range(N-1):
    focus_item = new_segments[i]
    mindist = math.inf

    for item in segments:
        dist = np.linalg.norm(focus_item['coords'] - item['coords'])
        if (dist < mindist):
            mindist = dist
            new_segments[i]['forward'] = np.asscalar(np.argwhere(segments==item))
            new_segments[i+1] = item

    segments = np.delete(segments, new_segments[i]['forward'])