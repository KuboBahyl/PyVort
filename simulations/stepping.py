#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 18:32:55 2017

@author: kubo
"""
def update_coords(segments, dt):
    for item in segments:
        item['coords'] += item['velocity_total'] * dt