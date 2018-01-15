#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 03:26:07 2017

@author: kubo
"""
import numpy as np

def fullLength(segments):
        length = 0
        for item in segments:
            if item['forward'] is not None:  
                nextItem = segments[item['forward']]
                dist = np.linalg.norm( item['coords'] - nextItem['coords'] )
                length += dist
        return length