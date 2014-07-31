""" Script that takes in lat,lon gps coordinates and returns the x,y coordinates."""
from pylab import *
from mpl_toolkits.basemap import Basemap
from varglas.data.data_factory    import DataFactory
from varglas.utilities            import DataInput
from fenics                       import *

# Get the Antarctica data sets
#bedmap2 = DataFactory.get_bedmap2()
#db2 = DataInput(bedmap2)

# Load the outlet glacier data
outlet_data = loadtxt('data/outlet_glaciers.out', delimiter = '|', dtype = 'str')
glacier_names = array(outlet_data[:,0], dtype = 'str')
glacier_lons = array(outlet_data[:,1], dtype = 'f')
glacier_lats = array(outlet_data[:,2], dtype = 'f')

# Setup the basemap projection
proj   = 'stere'
lat_0  = '-90'
lat_ts = '-71'
lon_0  = '0'
width = 3333500*2
height = 3333500*2

# Plot all the points
m = Basemap(width=width, height=height, resolution='h',
            projection="stere", lat_ts=lat_ts, lon_0=lon_0, lat_0=lat_0)

# Convert the glacier (lon, lat) coordinates to basemap coordinates
glacier_xs, glacier_ys = m(glacier_lons, glacier_lats)

m.drawcoastlines(linewidth=0.25, color = 'black') 
# Plot the glaciers
m.plot(glacier_xs, glacier_ys, 'ro', ms = 3)

# Plot ice mask contour
cont_data = loadtxt('data/cont_basemap.out')
m.plot(cont_data[:,0], cont_data[:,1], 'k--', linewidth = 0.25, dashes = (1,1))
show()
