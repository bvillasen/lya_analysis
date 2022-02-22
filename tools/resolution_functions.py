import os, sys
import numpy as np



def upscale_value( val, stride=4, log=True ):
  if log: val = np.log10(val)
  scale = np.abs( 0.0001*val )
  # vals = np.random.normal( loc=val, scale=scale, size=stride )
  vals = np.ones(stride) * val
  # print (vals)
  if log: vals = 10**vals
  return vals


def Upscale_Skewers_Data( skewers_data_subsampled, stride = 4 ):

  n_skewers, n_subsampled = skewers_data_subsampled['density'].shape
  field_list = skewers_data_subsampled.keys()

  fields_upscaled = {}
  for field in field_list:
    field_upscaled = []
    upscale_log = False
    # if field == 'velocity': upscale_log = False
    for skewer_id in range( n_skewers ):
      field_subsampled = skewers_data_subsampled[field][skewer_id]
      field_up = np.array([ upscale_value( val, stride=stride, log=upscale_log ) for val in field_subsampled ]).flatten()
      field_upscaled.append( field_up )
    field_upscaled = np.array( field_upscaled )
    fields_upscaled[field] = field_upscaled
  return fields_upscaled


def Subsample_Skewers_Data( skewers_data, stride = 4 ):

  n_skewers, n_points = skewers_data['density'].shape 
  n_sampled = n_points // stride  
  field_list = skewers_data.keys()
  fields_subsampled = {}
  for field in field_list:
    field_subsampled = []
    for skewer_id in range(n_skewers):
      data_field = skewers_data[field][skewer_id]
      data_subsampled = np.array([ data_field[i*stride:(i+1)*stride].mean()  for i in range(n_sampled) ])
      field_subsampled.append( data_subsampled )
    field_subsampled = np.array( field_subsampled )
    fields_subsampled[field] = field_subsampled
  return fields_subsampled
