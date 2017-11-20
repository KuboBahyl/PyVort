#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Vortex(object):
    # init constructor
    def __init__(self, name):
        self.name = name
        
    # representation
    def __repr__(self):
        return 'Quantum-Vortex-{!r}'.format(self.name)
    
    def __str__(self):
        return 'Quantum vortex of type - %s' % (self.name)
    

