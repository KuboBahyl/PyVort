#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 09:35:46 2017

@author: kubo
"""

#from vortices import Vortex
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np

# 3D example
total_rad = 1
z_factor = 3
noise = 0.01

num_true_pts = 100
s_true = np.linspace(0, total_rad, num_true_pts)
x_true = np.cos(s_true)
y_true = np.sin(s_true)
z_true = 1

num_sample_pts = 5
s_sample = np.linspace(0, total_rad, num_sample_pts)
x_sample = np.cos(s_sample) + noise * np.random.randn(num_sample_pts)
y_sample = np.sin(s_sample) + noise * np.random.randn(num_sample_pts)
z_sample = s_sample/z_factor + noise * np.random.randn(num_sample_pts)

tck, u = interpolate.splprep([x_sample,y_sample,z_sample], s=2)
#x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
u_fine = np.linspace(0,1,num_true_pts)
x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)

fig2 = plt.figure(2)
ax3d = fig2.add_subplot(111, projection='3d')
#ax3d.plot(x_true, y_true, z_true, 'b')
ax3d.plot(x_sample, y_sample, z_sample, 'r*')
#ax3d.plot(x_knots, y_knots, z_knots, 'go')
ax3d.plot(x_fine, y_fine, z_fine, 'g')
fig2.show()