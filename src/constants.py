#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 21:42:16 2017

@author: kubo
"""

quantum_vorticity = 9.97e-4 # cm^2/s
core_width = 1e-8 # cm

temps = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.05, 2.10, 2.15]

def get_mutual_coeffs(temperature):
    ind = temps.index(temperature)
    alpha1 = [0.006, 0.012, 0.023, 0.036, 0.052, 0.073, 0.098, 0.127, 0.161, 0.21, 0.29, 0.36, 0.50, 1.09]
    alpha2 = [0.003, 0.006, 0.011, 0.014, 0.017, 0.018, 0.016, 0.012, 0.008, 0.009, 0.011, 0.003, -0.03, -0.27]

    return alpha1[ind], alpha2[ind]

# density in kg/m^3
def get_densities(temperature):
    ind = temps.index(temperature)
    rho_tot = [145.1, 145.1, 145.1, 145.1, 145.1, 145.2, 145.2, 145.3, 145.4, 145.5, 0145.6, 145.7, 145.8, 146.0]
    rho_s = [144, 143, 141, 138, 134, 129, 121, 112, 99, 85, 64, 51, 37, 17]

    return rho_tot[ind], rho_s[ind]

# resulting LIA velocity is ~ kappa * 1/r = cm/s
# r/a should be >>1
