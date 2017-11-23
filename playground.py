#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 09:35:46 2017

@author: kubo
"""

from vortices import Vortex

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

testPositions = np.array([[x, 2*x, 5] for x in range(10)])

testVortex = Vortex(testPositions)