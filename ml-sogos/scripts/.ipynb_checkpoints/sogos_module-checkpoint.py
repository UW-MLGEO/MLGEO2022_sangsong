# SOGOS Module for MLGeo Analysis

# %% Import packages

import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cmocean import cm as cmo
from datetime import datetime
import scipy
import glidertools as gt

# %% Global variables you can import into your notebooks

# plt.rcParams['font.size'] = '12'
params = {'legend.fontsize': 12, \
          'xtick.labelsize':12, \
          'ytick.labelsize':12, \
          'font.size':12}
plt.rcParams.update(params)
pltsize=(10,5)

lims = {"SA" : [33.5, 35],
       "CT" : [1, 3.5],
       "oxygen" : [150, 350],
       "AOU" : [10, 120],
       "pH" : [7.63, 8.0],
       "TA" : [2280, 2387]}

palettes = {'SA': cmo.haline, 
        'CT': cmo.thermal, 
        'oxygen': cmo.ice, 
        'oxy_tcorr': cmo.ice, 
        'AOU': cmo.amp, 
        'pH': cmo.matter_r, 
        'TA': cmo.tempo}


# %% Common functions for operating on arrays
def datetime2ytd(time):
    """" Return time in YTD format from datetime format."""
    return (time - np.datetime64('2019-01-01'))/np.timedelta64(1, 'D')

def ytd2datetime(num):
    """" Return datetime format to YTD in 2019."""
    return (num * np.timedelta64(1,'D')) + np.datetime64('2019-01-01')



# %% Functions for operating on datasets

# Note: naming convention g3 comes from "gridded dataset - level 3"
# g3 can be gi_ or gp_ (iso or pressure)

def trim(g3, min=119, max=210, coord='days'):
    """ Return a trimmed dataset, good for testing code on a subset of dat. 
    @param      g3: gridded dataset (gp_ or gi_)
                coord: either 'days' by default or specify'nprof'
    @return     new xarray Dataset with trimmed data
    """
    #Interesting! Note that you have to do g3.coord.where and not just g3.where
    #Transposing above will make your grid return a weird pickle lock thread error.
    #Fixed below
    temp = g3[coord].where((g3[coord]>min) & (g3[coord]<max), drop=True)
    g3 = g3.sel(nprof=temp.nprof)

    return g3

def vert_profiles(g3):
    """"
    Returns a list of datasets, each corresponding to an interpolated vertical profile on one glider dive.

    @param      g3: gridded dataset (gp_ or gi_), for APL-processed L2 or L3 data. 
    @return     list of xarray Datasets
    """
    profiles = [] # initialize a list of datasets (each dataset will be one vertical profile ~ 1 glider dive)
    for idx, n in enumerate(g3.nprof):
        vert = g3.sel(nprof=n)   # vertical slice of the grid (profile over depth for one dive)
        profiles.append(vert)
    return profiles

# %% Plotting functions

def plot_var(g3_glider, var='SA'):
    """"
    Quick plot for single variable, for troubleshooting code.
    @param      gp_glider: gridded dataset
                var: Options are 'SA', 'CT', 'oxygen', 'AOU', 'spice'"""
    
    fig = plt.figure(figsize=(8,4))
    ax = fig.gca()
    g3_glider[var].plot(ax=ax, cmap=cmo.dense)

    ax.margins(x=0.01)
    ax.invert_yaxis()
    ax.set_xlabel('profile number')


def plotx_nprof(g3, vars = ['SA', 'CT'], tag='', save=False, lim=[]):
    """
    Plot over profile number. Faster than scatterplot by days because of Dataset format.
    @param  g3: Pass either gridded dataset gp_ on pressure, or gi_ on isopycnals.
            vars: Options are ['SA', 'CT', 'oxygen', 'AOU', 'spice']
    """
    for v in vars:
        fig = plt.figure(figsize=pltsize)
        ax = fig.gca()

        if len(lim)==0:
            min =  lims[v][0]
            max =  lims[v][1]
        else:
            min = lim[0]
            max = lim[1]
        c = palettes[v]

        g3[v].plot(vmin=min, vmax=max, cmap=c, ax=ax)

        ax.margins(x=0.01)
        ax.invert_yaxis()
        ax.set_title(v + ' ' + tag)
        ax.set_xlabel('profile number')

        pngtitle = tag + '_' + v + '_nprof.png'
        if save:
            plt.savefig('figures/' + pngtitle, format='png')

    return

def plotx_days(g3, ycoord='depth', vars = ['SA', 'CT'], tag='', save=False, lim=[]):
    """
    Plot over profile number. Faster than scatterplotting by days because of the Dataset format.
    @param  g3: Pass either gridded dataset gp_ on pressure, or gi_ on isopycnals.
            vars: Options are ['SA', 'CT', 'oxygen', 'AOU', 'spice'
            ycoord: Options are 'depth', 'sigma'
    """

    for v in vars:
        fig = plt.figure(figsize=(10,5))
        ax = fig.gca()

        if len(lim)==0:
            min =  lims[v][0]
            max =  lims[v][1]
        else:
            min = lim[0]
            max = lim[1]
        
        c = palettes[v]
        
        g3.plot.scatter('days', ycoord, hue=v, vmin=min, vmax=max, cmap=c, ax=ax, s=3, zorder=3)

        ax.margins(x=0.01)
        ax.invert_yaxis()
        ax.set_xlabel('days')
        ax.set_ylabel(ycoord)
        ax.set_title(v + ' ' + tag)
        plt.grid(visible=True, axis='x', zorder=0)

        # ax.set_xticks(np.arange(120,206,5))
        # for label in ax.xaxis.get_ticklabels()[::5]:
        #     label.set_visible(False)

        if ycoord=='depth':
            tg = 'gp' + tag
        elif ycoord=='sigma':
            tg = 'gi' + tag 
        pngtitle = tg + '_' + v + '_days.png'
        if save:
            plt.savefig('figures/' + pngtitle, format='png')

    return


