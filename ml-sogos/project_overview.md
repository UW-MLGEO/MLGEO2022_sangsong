# ML - SOGOS Overview

Song Sangmin <sangsong@uw.edu> <github: psmsong>

Joyce Cai 

UW Oceanography

Last updated: Oct 26 2022


## For joyce:

[Link to gridded variables](https://uwnetid-my.sharepoint.com/:f:/g/personal/sangsong_uw_edu/Et5YKAWyry5KkSst28_unxsBE3Vc5TCbOGl-3lR4sTvSQQ?email=joycecai%40uw.edu&e=einIE4)

		- `gp_659_forMLGeo1026.nc` 	(pressure-gridded 1m, glider #659)
		- `gp_660_forMLGeo1026.nc`	(pressure-gridded 1m, glider #660)

		- `gi_659_forMLGeo1026.nc`	(isopycnal-gridded .001, glider #659)
		- `gi_659_forMLGeo1026.nc`	(isopycnal-gridded .001, glider #659)


- See 

## Directions 

I recommend starting by opening sogos_main.ipynb. 
Each section in sogos_main.ipynb covers one step of analysis. Often the analysis is described or diagnosed in further detail in a separate notebook entitled `[method]_diagnostics.ipynb`. The main notebook starts with the 'L3' dataset ('level-3' processed dataset from APL, gridded and interpolated. See notes from Jeff Schilling, APL-UW, at bottom), performs corrections, then predicts variables.

 - `sogos_main.ipynb` : Main notebook outlining the analysis process. 
                        Each step in the analysis is shown, and some steps will reference other notebooks or algorithms. 

Many major functions are stored in modules, which are listed under the Code Directory.

- `sgmod_[purpose].py`: Modules are used to control processing functions required across multiple scripts.
                sgmod_main              Common glider functions like datetime handling
                sgmod_L3proc            Used for xarray Datset processing of the 'L3' grid
                sgmod_DFproc            Used for pandas Dataframe processing during analysis
                sgmod_plotting          Used to define common plotting parameters

Two phases of processing were developed externally in MATLAB: 

1. Oxygen optode time response correction (Adapted from Yui Takeshita, MBARI)
2. ESPER (Courtesy of Brendan Carter [Link to Github])


---
## Code Directory

**Folders**

- `data/` : float, ship, and glider data as downloaded
- `gridded-vars/`/ : calculated output variables from analysis
- `figures/` : useful diagnostic and analysis figures

---
**Modules**

                sgmod_main as sg                      ytd, profile splitting... 
                sgmod_L3proc as gproc                 grid Xarray processing - buoyancy, AOU, transform, dav-BFSLE
                sgmod_DFproc as dfproc                DataFrame processing - season, dav-MLD, T-S binning, ESPER
                sgmod_plotting as sgplot              plotting functions 

---
**Data/Variable Naming Conventions**
    
*Satellite:*    
 
                fsle_backwards                  map of daily FSLE snapshots
                satellite_data                  adt, geo velocities, ssh anomalies 
*Glider:*    
 
                gp_659                          L3 dataset gridded on pressure
                gi_659                          L3 dataset gridded on isopycnals
                dav_659                         L3 dive-averaged metrics, incl. MLD
                df_659                          Flattened dataframe for variable operations
    
 


 ---
 ## SOGOS_Apr19 L2 and L3 reprocessing notes

- owner: gbs2@uw.edu - 2021/09/24
- emailed to me (sangsong@uw.edu 2022/10/21)

## SG659
For SG659, glider .eng files for dives 27 through the end were reconstructed from scicon files for
depth and compass (see create_eng.py for details).  The following files:

sc0078b/psc6590078b_depth_depth.eng 
sc0096b/psc6590096b_depth_depth.eng 
sc0176b/psc6590176b_depth_depth.eng 
sc0332b/psc6590332b_depth_depth.eng 
sc0451b/psc6590451b_depth_depth.eng 
sc0476a/psc6590476a_depth_depth.eng 
sc0485a/psc6590485a_depth_depth.eng 

did not exist, so .eng files for those dives were not created.

## SG659 and SG660
Both glider data was the processed the IOP in-house version of the basestation
code.  This version is substantially the same as version 2.13 - released to
Hydroid in May of this year, but not yet available (that I know of).  The
primary change is the incorporation of the FMS system
(https://digital.lib.washington.edu/researchworks/handle/1773/44948) which
yields a number of improvements in the CTD corrections. 

The Hydroid version of the Seaglider flight code and basestation have some
differences in netcdf variable naming.  To process the optode and wetlabs data,
is renamed these variable columns - see the sg_calib_constants.m in both
gliders directories for the remapping scheme.

Unfortunately, our version of the basestation does not apply the PAR sensor
calibrations to the output, so the PAR data is as reported by the instrument.

## L23 Processing
To have a sanity check of the processing, I ran the re-processed data through
code to create L2 (1m binned) and L3 (interpolated with outliers removed) data
sets - see SOGO_Apr19_L23 for the data, and SOGO_Apr19_L23/plots for the output
plots. 

In both gliders data sets, something changed dramatically at the end of the
mission - for SG659 starting on dive 463 and for SG660 on dive 510, the
temperature jumps dramatically.  I didn't trace this all the way back to the
raw instrument output, but observed it is in the original netcdfs provided with
SG660, so I'm assuming this is a real and not processing related.

