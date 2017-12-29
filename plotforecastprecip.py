#!/glade/u/home/manab/anaconda3/bin/python

import sys
import xarray as xr
import glob, os
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # User supplied information
    indir = '/glade/p/work/manab/SHARP/MetSim/PNW/output/forecast/'
    spinup = '/glade/p/work/manab/SHARP/MetSim/PNW/output/spinup/20170101_20171127/spinup_total_summa.nc'
    hid = 17007554

    # Import forecast ensemble simulations
    forecastlist = glob.glob((indir+'*{}*.nc').format('summa'))   # Find all forecast files

    #for x in range(0, len(forecastlist)):
    #    ffile = os.path.splitext(os.path.basename(forecastlist[x]))[0]   #Get names of the forecast files
    #    ffile = xr.open_dataset(forecastlist[x])

    f0 = xr.open_dataset(forecastlist[0])
    f1 = xr.open_dataset(forecastlist[1])
    f2 = xr.open_dataset(forecastlist[2])
    f3 = xr.open_dataset(forecastlist[3])
    f4 = xr.open_dataset(forecastlist[4])
    f5 = xr.open_dataset(forecastlist[5])
    f6 = xr.open_dataset(forecastlist[6])
    f7 = xr.open_dataset(forecastlist[7])
    f8 = xr.open_dataset(forecastlist[8])
    f9 = xr.open_dataset(forecastlist[9])
    f10 = xr.open_dataset(forecastlist[10])
    f11 = xr.open_dataset(forecastlist[11])
    s = xr.open_dataset(spinup)
    s = s.loc['2017-10-01':'2017-11-26']
    # Plot

    (s.sel(hru = hid)['pptrate']*3600).plot()
    (f1.sel(hru = hid)['pptrate']*3600).plot()
    (f2.sel(hru = hid)['pptrate']*3600).plot()
    (f3.sel(hru = hid)['pptrate']*3600).plot()
    (f4.sel(hru = hid)['pptrate']*3600).plot()
    (f5.sel(hru = hid)['pptrate']*3600).plot()
    (f6.sel(hru = hid)['pptrate']*3600).plot()
    (f7.sel(hru = hid)['pptrate']*3600).plot()
    (f8.sel(hru = hid)['pptrate']*3600).plot()
    (f9.sel(hru = hid)['pptrate']*3600).plot()
    (f10.sel(hru = hid)['pptrate']*3600).plot()
    (f11.sel(hru = hid)['pptrate']*3600).plot()
    plt.ylabel('Precipitation Rate (mm/h)', fontsize=16)
    plt.xlabel('Time', fontsize=16)
    plt.savefig('pptrate.png')
    plt.show()
    
