import os, sys
import matplotlib
import matplotlib.pyplot as plt




def plot_power_spectrum( data_ps_plot, output_dir,  system='Shamrock', figure_name='flux_power_spectrum.png' ):
  
  if system == 'Lux' or system == 'Summit': matplotlib.use('Agg')


  fig_height = 10
  fig_width = 8
  fig_dpi = 300
  

  text_color = 'black'
  label_size = 18
  figure_text_size = 18
  legend_font_size = 16
  tick_label_size_major = 15
  tick_label_size_minor = 13
  tick_size_major = 5
  tick_size_minor = 3
  tick_width_major = 1.5
  tick_width_minor = 1
  border_width = 1

  if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=12)
  if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=12)
  matplotlib.rcParams['mathtext.fontset'] = 'cm'
  matplotlib.rcParams['mathtext.rm'] = 'serif'

    
  nrows = 1
  ncols = 1
  fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols*fig_width,fig_height*nrows))
  
  n_ps = len( data_ps_plot.keys()) - 1
  for index in range( n_ps ):
    k_vals = data_ps_plot[index]['k_vals']
    mean_ps = data_ps_plot[index]['mean']
    label = data_ps_plot[index]['label']
    if index == 2: ax.plot( k_vals, mean_ps, '--', lw=2, label=label )
    else: ax.plot( k_vals, mean_ps, lw=2, label=label )
  

  z = data_ps_plot['z']
  ax.text(0.90, 0.95, r'$z={0:.1f}$'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 

  ax.set_xscale('log')
  ax.set_yscale('log')
  
  ax.legend( loc=3, frameon=False, fontsize=16, prop=prop)

  [sp.set_linewidth(border_width) for sp in ax.spines.values()]

  
  ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
  ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')

  ax.set_ylabel( r' $\Delta_F^2(k)$', fontsize=label_size, color= text_color )
  ax.set_xlabel( r'$ k   \,\,\,  [\mathrm{s}\,\mathrm{km}^{-1}] $',  fontsize=label_size, color= text_color )



  fileName = output_dir + figure_name
  fig.savefig( fileName,  pad_inches=0.1, bbox_inches='tight', dpi=fig_dpi)
  print('Saved Image: ', fileName)
