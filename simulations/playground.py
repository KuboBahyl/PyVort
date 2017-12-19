#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 09:35:46 2017

@author: kubo
"""

from vortices import Vortex

import numpy as np

testPositions = np.array([[x, x**2, 0] for x in range(10)])
N = len(testPositions)

# init
testVortex = Vortex(testPositions)

# fixing neigbours for testline
testVortex.segments[0]['backward'] = None
testVortex.segments[N-1]['forward'] = None

# tests
testVortex.addProperties()
print(testVortex.segments)