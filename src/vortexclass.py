#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vortex class content:
    - constructor: assigns initial positions, relative position (neigbours) to each segment

    Methods:
    - get certain segment's coords
    - get all coords along certain direction {x,y,z}

"""
import numpy as np
from spline3D import spline3D

import finitediffs
from config import Config as cf
import constants as c

kappa = 10**8*c.quantum_vorticity # to um^2/s
a_core = 10**4*c.core_width # to um

# environment class - external sources of flow
class create_Env:
    def __init__(self, velocity_n_ext, velocity_s_ext):
        self.vel_n = np.array(velocity_n_ext)
        self.vel_s = np.array(velocity_s_ext)

    def evolute():
        # function how should external sources change in time
        pass

# vortex ring class - init only when simulation is focused on vortex rings
class create_Ring:
    def __init__(self, center, radius, direction):
        self.center = np.array(center)
        self.radius = radius
        self.direction = direction
        self.velocity = 0

# tangle o object containing all segmnets
class create_Vortex(object):

######################################
### INIT AND BASICS
######################################
    def __init__(self, coords):
        self.active_segments = len(coords)
        self.segments = np.array([
                {'is_active' : True,
                 'coords' : coords[i],
                 'backward' : i-1,
                 'forward' : i+1,
                 'tangent' : None,
                 'curvature' : None,
                 'velocity_LIA' : np.zeros(3),
                 'velocity_BIOT': np.zeros(3),
                 'velocity_drive' : np.zeros(3),
                 'velocity_full' : np.zeros(3)}
                 for i in range(self.active_segments)
                ])

        # boundary conditions for ring
        N = self.active_segments
        self.segments[0]['backward'] = N - 1
        self.segments[N-1]['forward'] = 0

    def __repr__(self):
        return 'Quantum Vortex object. Check documentation for available methods.'

    def go_backward(self, item):
        return self.segments[item['backward']]

    def go_forward(self, item):
        return self.segments[item['forward']]

######################################
### CALC METHODS
######################################

    def calc_derivative(self, item, order=1, neighbours=4):
        # start with the first item in range
        firstItem = self.go_backward(
                        self.go_backward(item))

        # extract coords from each item
        neighCoords = []
        thisItem = firstItem
        for i in range(5):
            neighCoords.append(thisItem['coords'])
            thisItem = self.go_forward(thisItem)

        # calculate coeffs for numeric derivative
        if (neighbours==4):
            coeffs = finitediffs.calc_FDcoeffs_closed(neighCoords, order)
        elif (neighbours>4):
            try:
                coeffs = finitediffs.calc_FDcoeffs_inverse(neighCoords, order)
            except:
                coeffs = finitediffs.calc_FDcoeffs_approx(neighCoords, order)


        derivative = coeffs.dot(neighCoords)
        return derivative

    def calc_velocity_LIA(self, item):
        if cf.use_LIA_updated:
            radius = 1 / np.linalg.norm(item['curvature'])
            beta = kappa * np.log(2*radius/a_core) / (4*np.pi)

        else:
            item_prev = self.go_backward(item)
            item_next = self.go_forward(item)
            len_prev = np.linalg.norm(item_prev['coords'] - item['coords'])
            len_next = np.linalg.norm(item_next['coords'] - item['coords'])

            log_term = np.sqrt(len_prev * len_next) / a_core
            beta = kappa * np.log(log_term) / (4*np.pi)

        v_lia = beta * np.cross(item['tangent'], item['curvature'])
        return v_lia

    def calc_velocity_BIOT(self, item):
        velocity_biot = np.zeros(3)

        for first_item in self.segments:
            if first_item['is_active']:
                second_item = self.go_forward(first_item)
                if second_item['is_active']:
                    if (first_item['forward'] != item['forward'] and second_item['forward'] != item['forward']):
                        R_first = first_item['coords'] - item['coords']
                        R_second = second_item['coords'] - item['coords']
                        R_first_len = np.linalg.norm(R_first)
                        R_second_len = np.linalg.norm(R_second)

                        first_term = (R_first_len + R_second_len) / (R_first_len * R_second_len)
                        second_term = np.cross(R_first, R_second) / (R_first_len * R_second_len + np.dot(R_first, R_second))

                        velocity_biot += kappa * first_term * second_term / (4 * np.pi)

        return velocity_biot

    def calc_velocity_drive(self, Env, item):
        v_n = Env.vel_n
        v_s = Env.vel_s

        v_ns = v_n - v_s
        v_i = item['velocity_LIA'] + item['velocity_BIOT']
        alpha1, alpha2 = c.get_mutual_coeffs(cf.temperature)

        v_drive1 = np.cross(item['tangent'], v_ns - v_i)
        v_drive2 = np.cross(item['tangent'], v_drive1)
        v_drive_full = alpha1*v_drive1 - alpha2*v_drive2
        return v_drive_full

    def calc_velocity_full(self, Env, item):
        v_s = Env.vel_s
        v_full = v_s + item['velocity_LIA'] + item['velocity_BIOT'] + item['velocity_drive']
        return v_full

######################################
### STRUCTURE METHODS
######################################

    def add_dumb_segment(self, coords, back, front):
        self.segments = np.append(self.segments,
                                  {'is_active': True,
                                   'coords' : coords,
                                   'backward' : back,
                                   'forward' : front,
                                   'tangent' : None,
                                   'curvature' : None,
                                   'velocity_LIA': np.zeros(3),
                                   'velocity_BIOT': np.zeros(3),
                                   'velocity_drive' : np.zeros(3),
                                   'velocity_full' : np.zeros(3)
                                   })

    def update_segments(self, Env, Ring):
        ind = ["x", "y", "z"].index(Ring.direction)
        other = np.delete(np.array([0,1,2]), ind)
        N = self.active_segments

        center, radius, velocity = np.zeros(3)

        for item in self.segments:
            if item['is_active']:
                # derivatives
                item['tangent'] = self.calc_derivative(item, order=1)
                item['curvature'] = self.calc_derivative(item, order=2)

                # normalisation
                norm = np.linalg.norm(item['tangent'])
                item['tangent'] /= norm
                item['curvature'] /= norm**2 # maybe not so useful

                # velocities
                item['velocity_LIA'] = self.calc_velocity_LIA(item)
                if cf.use_BIOT:
                    item['velocity_BIOT'] = self.calc_velocity_BIOT(item)
                if not cf.is_temp_zero:
                    item['velocity_drive'] = self.calc_velocity_drive(Env, item)
                item['velocity_full'] = self.calc_velocity_full(Env, item)

                center += item['coords'][ind] / N
                radius += np.sqrt(item['coords'][other[0]]**2 + item['coords'][other[1]]**2) / N
                velocity += item['velocity_full'][ind] / N

        Ring.center = center
        Ring.radius = radius
        Ring.velocity = velocity

    def update_connections(self):
        pass

    def update_segmentation(self, min_dist, max_dist):

        # assumes that segments are already reconnected = indices are assigned
        N = self.active_segments
        i = 0

        while (i < len(self.segments)):
            item = self.segments[i]
            i += 1

            if item['is_active']:
                next_item = self.go_forward(item)
                dist = np.linalg.norm(item['coords'] - next_item['coords'])

                if (dist < min_dist):
                    # make local interpolation with line using 4 points
                    item['coords'] = spline3D(self, item, next_item, type="nearest")

                    # update new neighbours
                    item['forward'] = next_item['forward']
                    next_next_item = self.go_forward(next_item)
                    next_next_item['backward'] = next_item['backward']

                    # making next_item inactive
                    next_item['is_active'] = False

                    N -= 1

                elif (dist > max_dist):
                    # make local interpolation with line using 4 points
                    new_point = spline3D(self, item, next_item, type="every_second")

                    # add new segment along the distant ones
                    self.add_dumb_segment(coords=new_point,
                                          back=next_item['backward'],
                                          front=item['forward'])
                                          
                    # update indices of new neighbours
                    newitem_index = len(segments) - 1
                    item['forward'] = newitem_index
                    next_item['backward'] = newitem_index

                    N += 1

        # making sure of boundaries
        #N = len(segments)
        #segments[0]['backward'] = N - 1
        #segments[N-1]['forward'] = 0

        # Vortex updates
        self.active_segments = N

######################################
### EXTRACTION OPTIONS
######################################

    # get coords of all segments
    def getAllCoords(self, index):
        return [item['coords']
                for item in self.segments]

    # get particular axis' coords of all segments
    # allowed input: "x", "y" or "z"
    def getAxisCoords(self, axis):
        ind = ["x", "y", "z"].index(axis)
        return [item['coords'][ind]
                for item in self.segments
                if item['is_active'] == True]
