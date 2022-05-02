import os, sys
from pathlib import Path
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_data import Load_Skewers_File

input_dir = '/data/groups/comp-astro/bruno/cosmo_sims/2048_50Mpc_V22/skewers_files/'

n_file = 55

axis_list = [ 'x', 'y', 'z' ]
field_list = [ 'density', 'HI_density', 'los_velocity', 'temperature' ]
skewer_dataset = Load_Skewers_File( n_file, input_dir, axis_list=axis_list, fields_to_load=field_list )

density = skewer_dataset['density']
HI_density = skewer_dataset['HI_density']
temperature = skewer_dataset['temperature']
los_velocity = skewer_dataset['los_velocity']
