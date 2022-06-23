import os, sys
from pathlib import Path
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_data import load_snapshot_data_distributed

data_dir = '/data/groups/comp-astro/bruno/'
sim_dir    = data_dir + f'cosmo_sims/2048_50Mpc_V22/'
input_dir  = sim_dir + 'snapshot_files/'
  
Lbox = 50000.0 #kpc/h
n_points = 2048
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_points, n_points, n_points ]
precision = np.float64

slice_depth = 16
subgrid = [ [0, slice_depth], [0, n_points], [0, n_points] ]

snap_id = 169
data_type = 'hydro'
fields = [ 'density', 'HI_density', 'momentum_z', 'temperature' ]
data_slice = load_snapshot_data_distributed( data_type, fields, snap_id, input_dir, box_size, grid_size,  precision, subgrid=subgrid, show_progess=True )
current_z = data_slice['Current_z']
slice_density = data_slice['density']
slice_HI_density = data_slice['HI_density']
slice_los_velocity = data_slice['momentum_z'] / slice_density 
slice_temepature = data_slice['temperature']


# skewer (i, j) from the slice
i, j, = 10, 1024
skewer_density = slice_density[i, j, :]
skewer_HI_density = slice_HI_density[i, j, :]
skewer_los_velocity = slice_los_velocity[i, j, :]
skewer_temperature = slice_temepature[i, j, :]
