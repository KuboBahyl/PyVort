#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 21:42:16 2017

@author: kubo
"""

quantum_vorticity = 9.97e-4 # cm^2/s
vortex_width = 1e-8 # cm = 0.1nm

# density in g/cm^3
def get_mutual_coeffs(temperature):
    temps = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.05, 2.10, 2.15]
    ind = temps.index(temperature)
    #rho_tot = [0.1451, 0.1451, 0.1451, 0.1451, 0.1451, 0.1452, 0.1452, 0.1453, 0.1454, 0.1455, 0.1456, 0.1457, 0.1458, 0.1460]
    #rho_s = [0.144, 0.143, 0.141, 0.138, 0.134, 0.129, 0.121, 0.112, 0.099, 0.085, 0.064, 0.051, 0.037, 0.017]
    alpha1 = [0.006, 0.012, 0.023, 0.036, 0.052, 0.073, 0.098, 0.127, 0.161, 0.21, 0.29, 0.36, 0.50, 1.09]
    alpha2 = [0.003, 0.006, 0.011, 0.014, 0.017, 0.018, 0.016, 0.012, 0.008, 0.009, 0.011, 0.003, -0.03, -0.27]

    return alpha1[ind], alpha2[ind]

# resulting LIA velocity is ~ kappa * 1/r = cm/s
# r/a should be >>1
