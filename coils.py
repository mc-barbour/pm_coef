# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 09:41:26 2022

@author: barbourm
"""
import numpy as np

class Coil():
    """
    Coil class. Initiate by defining the coil diameter, length, and number (all in units of m)
        
    Coil diameters by brand/type:
    360 Soft (2-5mm) : 0.2413
    Target 3D, 360 standard (3-5mm), 360 soft (6-14mm), 360/helical ultra, 360/helical nano : 0.254mm
    360 standard (6-10mm) : 0.2794mm
    360 standard (11-15mm): 0.3048mm
    Target XL (360 Standard/Soft, Helical) : 0.3556mm

    
    """
    
    def __init__(self, coil_type, length):
        
        self.coil_type = coil_type
        self.length = length
        self.coil_name, self.curvature = self.clean_coil_type()
        self.diameter = self.find_coil_diameter()*1e-3


    def clean_coil_type(self):
        
        coil_string = self.coil_type.split(" ")
        curvature = float(coil_string[-1].split("mm")[0])
        if coil_string[0] == "":
            coil_name = " ".join(coil_string[1:-1])
        else:
            coil_name = " ".join(coil_string[0:-1])
        
        return coil_name.lower(), curvature


    def find_coil_diameter(self):
        
        diameter_dictionary = {"target 3D": 0.254,
                               "target 360 soft small": 0.2413,
                               "target 360 soft large": 0.254,
                               "target 360 ultra": 0.254,
                               "target helical ultra": 0.254,
                               "target 360 nano": 0.254,
                               "target helical nano": 0.254}
        
        multi_diameter_coils_list = ["Target 360 soft", "Target 360 standard"]
        
        if self.coil_name in multi_diameter_coils_list:
            
            if self.coil_name == "Target 360 soft":
                if self.curvature <= 5:
                    self.coil_name = self.coil_name + " small"
                elif 6 <= self.curvature <= 14:
                    self.coil_name = self.coil_name + " large"
            
        
        
        if self.coil_name in diameter_dictionary:
            diameter = diameter_dictionary[self.coil_name]
            print('Found coil type. Assigning {:0.5f} mm for diameter of {:s}'.format(diameter, self.coil_name))
        else:
            
            raise ValueError("Coil type {:s} is not found in dictionary. Update dict or check input file".format(self.coil_name))
         
        return diameter
    
    def compute_coil_volume(self):
        volume = np.pi * self.diameter**2 / 4. * self.length
        return volume      
    
    def compute_coil_surfacearea(self):
        surface_area = np.pi * self.diameter * self.length
        return surface_area
