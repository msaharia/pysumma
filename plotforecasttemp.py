#!/glade/u/home/manab/anaconda3/bin/python

import sys
import xarray as xr
import glob, os
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # User supplied information
    indir = '/glade/p/work/manab/SHARP/MetSim/PNW/output/forecast/'
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

    # Plot
    (f1.sel(hru = hid)['temp']-272.15).plot()
    (f2.sel(hru = hid)['temp']-272.15).plot()
    (f3.sel(hru = hid)['temp']-272.15).plot()
    (f4.sel(hru = hid)['temp']-272.15).plot()
    (f5.sel(hru = hid)['temp']-272.15).plot()
    (f6.sel(hru = hid)['temp']-272.15).plot()
    (f7.sel(hru = hid)['temp']-272.15).plot()
    (f8.sel(hru = hid)['temp']-272.15).plot()
    (f9.sel(hru = hid)['temp']-272.15).plot()
    (f10.sel(hru = hid)['temp']-272.15).plot()
    (f11.sel(hru = hid)['temp']-272.15).plot()
    plt.ylabel('Temperature (C)', fontsize=16)
    plt.xlabel('Time', fontsize=16)
    plt.savefig('temp.png')
    plt.show()
    
