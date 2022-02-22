import numpy as np


def get_skewer_flux_fft_amplitude( vel_Hubble, delta_F ):
  n = len( vel_Hubble )
  dv = ( vel_Hubble[-1] - vel_Hubble[0] ) / n
  k_vals = 2 *np.pi * np.fft.fftfreq( n, d=dv )
  ft = 1./n * np.fft.fft( delta_F )
  ft_amp2 = ft.real * ft.real + ft.imag * ft.imag
  return k_vals, ft_amp2  



def get_skewer_flux_power_spectrum( vel_Hubble, delta_F, d_log_k=None, n_bins=None, k_edges=None ):
  n = len(vel_Hubble)
  dv = vel_Hubble[1] - vel_Hubble[0]
  vel_max = n * dv

  k_vals, ft_amp2 = get_skewer_flux_fft_amplitude( vel_Hubble, delta_F )

  indices = k_vals > 0
  k_vals = k_vals[indices]
  ft_amp2 = ft_amp2[indices]

  k_min = k_vals.min()
  k_max = k_vals.max()
  if d_log_k != None: 
    # intervals_log = np.arange( np.log10(k_min), np.log10(k_max), d_log_k )
    # intervals = 10**(intervals_log)
    k_min = np.log10( k_min )
    k_max = np.log10( k_max )
    k_start = np.log10( 0.99 * k_vals.min() )
    n_hist_edges = 1
    k_val = k_start
    while k_val < k_max:
      n_hist_edges += 1
      k_val += d_log_k
    hist_edges = []
    k_val = k_start
    for i in range( n_hist_edges ):
      hist_edges.append( 10**k_val )
      k_val += d_log_k
    intervals = np.array( hist_edges )
  elif n_bins  != None: intervals = np.logspace( np.log10(k_min), np.log10(k_max), n_bins )
  else: intervals = k_edges
  

  power, bin_edges= np.histogram( k_vals, bins=intervals, weights=ft_amp2 )
  n_in_bin, bin_edges = np.histogram( k_vals, bins=intervals )
  n_in_bin = n_in_bin.astype('float')
  bin_centers = np.sqrt(bin_edges[1:] * bin_edges[:-1])
  indices = n_in_bin > 0
  bin_centers = bin_centers[indices]
  power = power[indices]
  n_in_bin = n_in_bin[indices]
  power_avrg = power / n_in_bin * vel_max
  return bin_centers, power_avrg


def Compute_Flux_Power_Spectrum( data_Flux ):
  skewers_Flux = data_Flux['skewers_Flux']
  Flux_mean = data_Flux['Flux_mean']
  vel_Hubble = data_Flux['vel_Hubble']
  n_skewers = skewers_Flux.shape[0]

  # Compute the Power Spectrum from the Flux
  d_log_k = 0.1
  print( '\nComputing Flux Power Spectrum')
  skewers_power_spectrum = []
  for skewer_id in range(n_skewers):
    flux = skewers_Flux[skewer_id]
    delta_flux = flux / Flux_mean 
    k_vals, flux_power_spectrum = get_skewer_flux_power_spectrum( vel_Hubble, delta_flux, d_log_k=d_log_k )
    flux_power_spectrum = flux_power_spectrum * k_vals / np.pi
    skewers_power_spectrum.append( flux_power_spectrum )

  skewers_power_spectrum = np.array( skewers_power_spectrum ) 
  mean_power_spectrum = skewers_power_spectrum.mean( axis=0 ) 
  data_ps = { 'mean':mean_power_spectrum, 'k_vals':k_vals }
  return data_ps
