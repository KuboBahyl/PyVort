#!/usr/bin/env python3
#coding: utf-8
#%%
from vortices import Vortex

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

## VORTEX RING, T=0
N=100

radius = 1                #ring radius [A]
X0 = Y0 = Z0 = 0          #ring center coords [A]
R0 = np.array([X0,Y0,Z0])
phi = 2*np.pi/N

ringPositions = np.array([ R0 + [0, radius*np.sin(i*phi), radius*np.cos(i*phi)] 
                           for i in range (N)
                          ])
#%%


## INITIALISATION
Rvortex = Vortex(ringPositions)

# fixing neigbours for ring
Rvortex.segments[0]['backward'] = N - 1
Rvortex.segments[N-1]['forward'] = 0

# adding properties
Rvortex.addProperties()



#%%
mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(Rvortex.getAllAxisCoords(0), 
           Rvortex.getAllAxisCoords(1), 
           Rvortex.getAllAxisCoords(2), 
           label='ring')
ax.legend()

plt.show()

## saving vortex state
##