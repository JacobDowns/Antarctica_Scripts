""" Script that takes in lat,lon gps coordinates and returns the x,y coordinates."""
from pylab import *
from mpl_toolkits.basemap import Basemap
from varglas.data.data_factory    import DataFactory
from varglas.utilities            import DataInput
from fenics                       import *

# Get the Antarctica data sets
bedmap2 = DataFactory.get_bedmap2()
db2 = DataInput(bedmap2)

# Load the domain coordinates
domain_coords = loadtxt('data/new_domain.out')
domain_lons, domain_lats = db2.p(domain_coords[:,0], domain_coords[:,1], inverse = True)

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

# Convert the domain (lon, lat) coordinates to basemap coordinates
domain_xs, domain_ys = m(domain_lons, domain_lats)
# Close the rectangle
domain_xs = append(domain_xs, domain_xs[0])
domain_ys = append(domain_ys, domain_ys[0])

m.drawcoastlines(linewidth=0.25, color = 'black') 
# Plot the domain
m.plot(domain_xs, domain_ys, 'ro-', ms = 4)

# Plot ice mask contour
cont_data = loadtxt('data/cont_basemap.out')
m.plot(cont_data[:,0], cont_data[:,1], 'k--', linewidth = 0.25, dashes = (1,1))
show()
