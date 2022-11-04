# ML - SOGOS Overview

Song Sangmin <sangsong@uw.edu> <github: psmsong>

Joyce Cai <joycecai@uw.edu>	<github: JoyceCaiOcean>

UW Oceanography

Last updated: Oct 31 2022


## For Joyce:

[Link to gridded variables](https://uwnetid-my.sharepoint.com/:f:/g/personal/sangsong_uw_edu/Et5YKAWyry5KkSst28_unxsBE3Vc5TCbOGl-3lR4sTvSQQ?email=joycecai%40uw.edu&e=einIE4)

		- `gp_659_forMLGeo1026.nc` 	(pressure-gridded 1m, glider #659)
		- `gp_660_forMLGeo1026.nc`	(pressure-gridded 1m, glider #660)

		- `gi_659_forMLGeo1026.nc`	(isopycnal-gridded .001, glider #659)
		- `gi_659_forMLGeo1026.nc`	(isopycnal-gridded .001, glider #659)

                - 'fsle_backwards.nc'           (1-day FSLE from AVISO)
                - 'satellite_data.nc'           (ADT product from AVISO)

- Description of glider data variables in `Seaglider_DataGuide.pdf`

- First paper from SOGOS program: [Link to Dove (2021)](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2021JC017178)

- I recommend starting to look at the glider data by opening sogos_overview.ipynb. 
Right now the notebook only contains a few things, but we can add more sections as needed. 

The main notebook starts with the 'L3' glider datasets ('level-3' processed dataset from APL, gridded and interpolated. See notes from Jeff Schilling, APL-UW, at bottom) which have already been processed into "gp" (gridded-pressure) and "gi" (gridded-isopycnal) xarray Datasets.

Many major functions are stored in modules, which are also listed under the Code Directory.

- `sgmod_[purpose].py`: Modules are used to control processing functions required across multiple scripts.
                sgmod_main              Common glider functions like datetime handling
                sgmod_L3proc            Used for xarray Datset processing of the 'L3' grid
                sgmod_DFproc            Used for pandas Dataframe processing during analysis
                sgmod_plotting          Used to define common plotting parameters


The other option I'm thinking of sounds more promising, and involves satellite data that could be more interesting to your eddy research also! This is maybe more data clean-up, which could actually be useful as we both get familiar with formatting and manipulation of datasets in python. 

A different clustering method would use AVISO satellite products, which are more commonly used as an eddy metric.
1. First axis: Calculate SLA above the glider point in space i.e. latitude/longitude. (Download from AVISO)
    - Possible that SLA will not work well for clustering-- can explain further in person. Has to do with averaging where the product "SLA" = ADT - <long-term ADT> provided by AVISO uses a climatological mean <ADT>, which can interfere with the calculation for transient eddies. 
    - So a better variable could be a different metric -- SSH contours, or manually calculated SSH anomalies. A manual calculation of local-SSH = ADT - <ADT over 10 days> is more appropriate for high-latitude regions where the sea level is highly variable across time periods. 
2. Second axis: Some metric of mixing, like MLD or vertical gradient in spice from the glider data at that location. 
3. Clustering may show points in space that tend to be clustered with a strong vertical gradient and a specific SSH. 
        - If we want to save on time, we can definitely just do SLA and MLD (easiest to cluster on) as our axes. These wouldn't take long, and if they are bad to cluster on we can conclude that it may not be a good metric for the reasons above. But if the coding seems manageable in time, I would be interested in the other metrics. 
        - One theoretical motivation could be, is a higher SSH anomaly --> larger gradients? OR, could it be that smaller anomalies relate to spaces "in-between" eddies that seems to produce a lot of stirring.

---
## Code Directory

**Folders**

- `scripts/` : float, ship, and glider data as downloaded
- `figures/` : useful diagnostic and analysis figures

I recommend making a `data/` folder in your remote copy (on your laptop).
Large files won't upload to github so you can add the data/ folder to your .gitignore file.

---
**Modules**

                sogos_module as sg                      useful common functions + plotting

---
**Data/Variable Naming Conventions**

*Glider:*    
 
                gp_659                          L3 dataset gridded on pressure
                gi_659                          L3 dataset gridded on isopycnals
                dav_659                         L3 dive-averaged metrics, incl. MLD
                df_659                          Flattened dataframe for variable operations
    
 

Two phases of processing were developed externally in MATLAB.
1. Oxygen optode time response correction (Adapted from Yui Takeshita, MBARI)
2. ESPER (Courtesy of Brendan Carter [Link to Github])

 ---
 ## SOGOS_Apr19 L2 and L3 reprocessing notes from APL

- owner: Geoff Schilling gbs2@uw.edu - 2021/09/24
- documentation emailed to me (sangsong@uw.edu 2022/10/21)

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

