import os, sys
import numpy as np
import h5py as h5
root_dir = os.getcwd() + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_skewers import load_skewers_multiple_axis
from spectra_functions import Compute_Skewers_Transmitted_Flux
from flux_power_spectrum import Compute_Flux_Power_Spectrum
from plotting_functions import plot_power_spectrum
from resolution_functions import Subsample_Skewers_Data, Upscale_Skewers_Data

uvb = 'pchw18'

# dataDir = '/home/bruno/Desktop/ssd_0/data/'
# dataDir = '/data/groups/comp-astro/bruno/'
dataDir = '/raid/bruno/data/'
simulation_dir = dataDir + 'cosmo_sims/2048_hydro_50Mpc/'
input_dir = simulation_dir + 'skewers_{0}/'.format(uvb)
output_dir = simulation_dir + 'figures/'
create_directory( output_dir )

# Box parameters
Lbox = 50000.0 #kpc/h
nPoints = 2048
nx = nPoints
ny = nPoints
nz = nPoints
ncells = nx * ny * nz
box = {'Lbox':[ Lbox, Lbox, Lbox ] }

# Cosmology parameters
cosmology = {}
cosmology['H0'] = 67.66 
cosmology['Omega_M'] = 0.3111
cosmology['Omega_L'] = 0.6889


n_skewers_total = 1800
n_skewers_axis = n_skewers_total// 3 
n_skewers_list = [ n_skewers_axis, n_skewers_axis, n_skewers_axis ]
axis_list = [ 'x', 'y', 'z' ]


n_snapshot = 169
print(f"\nComputing LOS tau, s_nap:{n_snapshot}   n_skewers:{n_skewers_total}" )

field_list = [ 'density', 'HI_density', 'velocity', 'temperature' ]

skewer_dataset = load_skewers_multiple_axis( axis_list, n_skewers_list, n_snapshot, input_dir,  set_random_seed=False, print_out=True ) 
current_z = skewer_dataset['current_z']
cosmology['current_z'] = current_z
skewers_data = { field:skewer_dataset[field] for field in field_list }
data_Flux = Compute_Skewers_Transmitted_Flux( skewers_data, cosmology, box )
data_ps = Compute_Flux_Power_Spectrum( data_Flux )
data_ps['label'] = 'Simulation'

skewers_data_subsampled = Subsample_Skewers_Data( skewers_data )
data_Flux_subsampled = Compute_Skewers_Transmitted_Flux( skewers_data_subsampled, cosmology, box )
data_ps_subsampled = Compute_Flux_Power_Spectrum( data_Flux_subsampled )
data_ps_subsampled['label'] = 'Down-sampled'

skewers_data_upsampled = Upscale_Skewers_Data( skewers_data_subsampled )
data_Flux_upsampled = Compute_Skewers_Transmitted_Flux( skewers_data_upsampled, cosmology, box )
data_ps_upsampled = Compute_Flux_Power_Spectrum( data_Flux_upsampled )
data_ps_upsampled['label'] = 'Up-sampled'


data_ps_plot = {}
data_ps_plot['z'] = current_z
data_ps_plot[0] = data_ps
data_ps_plot[1] = data_ps_subsampled
data_ps_plot[2] = data_ps_upsampled

figure_name = f'power_spectrum_flat_n{n_skewers_total}.png'
plot_power_spectrum( data_ps_plot,  output_dir,  system='Shamrock', figure_name=figure_name )


