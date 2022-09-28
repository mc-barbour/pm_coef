# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 09:43:32 2022

@author: barbourm
"""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

from coils import *

#%% open file

root = tk.Tk()
root.title("Select coil param file")
root.resizable(False, False)
root.geometry("300x150")

def select_file():
    
    filetypes = (
        ('text files', "*.txt"),
        ("all files", "*.*")
        )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir = 'C:',
        filetypes=filetypes
        )
    showinfo(
        title='Selected File',
        message=filename
        )
    
open_button = ttk.Button(
    root,
    text="Open File",
    command=select_file
    )

open_button.pack(expand=True)
root.mainloop()
#%% Load the coil params file

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
filename = open_file()
quit_tk()

window.mainloop()



#%% Figure out parsing of coil text string

with open(filename) as f:
    coil_txt = f.readlines()
    if len(coil_txt) != 2:
        raise ValueError("More than 1 line in coil param text file")

#%%
def clean_coil_type(coil_type):
    
    coil_string = coil_type.split(" ")
    curvature = coil_string[-1]
    if coil_string[0] == "":
        coil_name = " ".join(coil_string[1:-1])
    else:
        coil_name = " ".join(coil_string[0:-1])
    
    return coil_name, curvature


#%% Create list of coils

coil_params_list = coil_txt[0].split(",")
volume_aneurysm = float(coil_txt[1].split("=")[-1])
coils = []
for coil_params in coil_params_list:
    coil_type, length_string = coil_params.split(" x ")
    length = float(length_string.split("cm")[0])*1e-2
    # print(coil_type, length)
    coils.append(Coil(coil_type, length))
    

#%% Compute loss coefficients
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

# with open('D:\Barbour\Aneurysm\Patients\S115\Simulation\simplePM_coef.txt','w') as f:
#     f.write("Viscous Resistance: {:10.5f} \nInertial Resistance: {:10.5f} \nPorosity: {:10.3f}%".format(viscous_resistance, inertial_resistance, porosity))
