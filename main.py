#!/usr/bin/env python3
#coding: utf-8

import numpy as np
from matplotlib import pyplot as plt

class vortex():
    # init constructor
    def __init__(self, name):
        self.name = name
        
    # representation
    def __repr__(self):
        return 'Quantum_Vortex-{!r}'.format(self.name)
    
    
        


v1 = vortex('Kubo')