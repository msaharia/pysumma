#!/glade/u/home/manab/anaconda3/bin/python

import sys
import xarray as xr
import numpy as np
import glob, os
from functools import reduce #for custom search strings

if __name__ == "__main__":
    # User supplied information
    outdir = '/glade/p/work/manab/SHARP/PNW_3L/output/paramtest3_out/'                   #Directory containing SUMMA output
    convertdir = '/glade/p/work/manab/SHARP/PNW_3L/output/paramtestconvert3/'
    concatdir = '/glade/p/work/manab/SHARP/PNW_3L/output/paramtestconcat3/'
    finalfile = 'paramtest3.nc'
    restartfile = 'forecastrestart.nc'
    restartstring = 'summaRestart_2017-11-26'
    
    startGRU = 1                              #Start GRU Index
    endGRU = 11723                            #End GRU Index
    lenGRU = 50                               #Length of every GRU string
    
    # Step 1: Convert all SUMMA output files into HRU-only
    outfilelist = glob.glob((outdir+'/*.nc')) #list of all files
    outfilelist = [x for x in outfilelist if "summaRestart" not in x] #Remove Restart files

    for x in range(0, len(outfilelist)):
        ncconvert = xr.open_dataset(outfilelist[x])                                  #Import netCDF file

        runoffdata = ncconvert['averageInstantRunoff'].values                     #Extract averageInstantRunoff values
        runoffarray = xr.DataArray(runoffdata, dims=['time','hru'])            #Create an array of averageInstantRunoff with 2 dimensions
        ncconvert = ncconvert.drop('averageInstantRunoff')                           #Drop the original averageInstantRunoff variable
        ncconvert['averageInstantRunoff'] = runoffarray                           #Add the new array to original netCDF
        ncconvert['averageInstantRunoff'].attrs['long_name'] = "instantaneous runoff (instant)"
        ncconvert['averageInstantRunoff'].attrs['units'] = '-'

        baseflowdata = ncconvert['basin__AquiferBaseflow'].values                     #Extract basin__AquiferBaseflow values
        baseflowarray = xr.DataArray(baseflowdata, dims=['time','hru'])            #Create an array of basin__AquiferBaseflow with 2 dimensions
        ncconvert = ncconvert.drop('basin__AquiferBaseflow')                           #Drop the original averageInstantRunoff variable
        ncconvert['basin__AquiferBaseflow'] = baseflowarray                           #Add the new array to original netCDF
        ncconvert['basin__AquiferBaseflow'].attrs['long_name'] = "baseflow from the aquifer (instant)"
        ncconvert['basin__AquiferBaseflow'].attrs['units'] = 'm s-1'

        print('Step 1: Creating '+str(x+1)+ ' HRU-only SUMMA output file out of ' + str(len(outfilelist)))
        ncconvert_outfile = os.path.join(convertdir, os.path.basename(outfilelist[x]))#Create an output filename
        ncconvert.to_netcdf(ncconvert_outfile, 'w')                                  #Write out the final netCDF file


    # Step 2: Concatenate each GRU set by time

    # Create search strings for GRU sets in SUMMA output
    slist = np.arange(startGRU, endGRU, lenGRU)   #Searchlist for start indices
    elist = slist + lenGRU - 1                    #Searchlist for end indices
    elist[-1] = endGRU                            #Replace last end index

    slist = np.char.zfill(slist.astype(str), 5)
    elist = np.char.zfill(elist.astype(str), 5)
    selist = ['G', slist, '-', elist]         
    gruset = reduce(np.char.add, selist)

    outdirsearch = convertdir+'*{}*.nc'
 
    #Concatenate by time 
    for x in range(0, len(slist)):
        timefilelist = glob.glob((convertdir+'/*{}*.nc').format(gruset[x])) #list of all files

        ncconcat_time = xr.open_mfdataset(timefilelist, concat_dim='time')     #Concatenates by time
        ncconcat_time = ncconcat_time.sortby('time')                           #Sorts by time
        ncconcat_time['hruId'] = ncconcat_time['hruId'].isel(time=0, drop=True)  #Dropping extra time dimension from hruId

        print('Step 2: Concatenating GRUset '+str(x)+ ' of ' + str(len(slist)))
        timeconcatfile = os.path.join(concatdir, (gruset[x]+'.nc'))
        ncconcat_time.to_netcdf(timeconcatfile, 'w')

    #Part 3: Conatenate each GRU set in space

    spacefilelist = glob.glob(concatdir+'/*.nc')
    spacefilelist.sort()
    print('Step 3: Concatenating by HRU space')
    ncconcat_space = xr.open_mfdataset(spacefilelist, concat_dim='hru')
    #ncconcat_space['hruId'] = ncconcat_space['hruId'].isel(time=0, drop=True)  #Dropping extra time dimension from hruId

    finalfilename = os.path.join(concatdir, finalfile)
    ncconcat_space.to_netcdf(finalfilename, 'w')


