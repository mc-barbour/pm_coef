# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 09:43:32 2022

@author: barbourm

Compute the inertial and viscous loss coefficients for a coiled aneurysm

Input is a text file that contains a list of the inserted coils on the first line. 
The second line contains the aneurysm volume in cubic meters

An example file is found in coil_params.txt in this directory
"""
from pathlib import Path

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

from coils import *



#%% Functions

# create tkinter window
window = tk.Tk()
window.geometry("700x300")

tk.Label(
    window, 
    text="Open the coil parameters file",
    )

def open_file():
    
    filetypes = (
        ('text files', "*.txt"),
        ("all files", "*.*")
        )

    filename = fd.askopenfilename(
        title='Open a file',
        filetypes=filetypes
        )
    return filename

def quit_tk():
    window.destroy()


def create_coil_list(coil_txt):
    """
    Parse the input file and initialize the list of coils 
    """
    coil_params_list = coil_txt[0].split(",")
    volume_aneurysm = float(coil_txt[1].split("=")[-1])
    coils = []
    for coil_params in coil_params_list:
        coil_type, length_string = coil_params.split(" x ")
        length = float(length_string.split("cm")[0])*1e-2
        coils.append(Coil(coil_type, length))
    
    return coils


def loss_coefficients(coils, input_file):
    """
    Compute the viscous and inertial loss coefficients. 
    Save the information in the same directory where the input file was opened from

    """
    c=2
    total_coil_volume = 0
    surface_area_ratio = 0
    
    for coil in coils:
    
        volume = coil.compute_coil_volume()
        print(volume)
        total_coil_volume += volume
        
        surface_area = coil.compute_coil_surfacearea()
        surface_area_ratio += surface_area / volume_aneurysm
        
    print("Total Coil Volume: {:10.4f} (mm)".format(total_coil_volume*1e9))
    
    packing_density = total_coil_volume / volume_aneurysm
    porosity = 1 - packing_density
    
    k = porosity**3 / (c*surface_area_ratio**2)
    
    viscous_resistance = 1. / k
    
    inertial_resistance = packing_density * (296 - 40.9) / (.28 - 0.11)
    
    print("Viscous Resistance: {:10.5f} \nInertial Resistance: {:10.5f} \nPorosity: {:10.3f}%".format(viscous_resistance, inertial_resistance, porosity))
    
    outfile = Path(input_file).parent / "fluent_porous_media_coef.txt"
    
    with open(outfile,'w') as f:
        f.write("Viscous Resistance: {:10.5f} \nInertial Resistance: {:10.5f} \nPorosity: {:10.3f}%".format(viscous_resistance, inertial_resistance, porosity))
        

#%% Main function

def main():
    
    filename = open_file()
    quit_tk()
    window.mainloop()
    
    with open(filename) as f:
        coil_txt = f.readlines()
        if len(coil_txt) != 2:
            raise ValueError("More than 1 line in coil param text file")
            
    coil_list = create_coil_list(coil_txt)
    loss_coefficients(coil_list, filename)
    
    
main()
    

    