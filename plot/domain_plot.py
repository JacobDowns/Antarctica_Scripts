""" Script that takes in lat,lon gps coordinates and returns the x,y coordinates."""
from pylab import *
from mpl_toolkits.basemap import Basemap
from varglas.data.data_factory    import DataFactory
from varglas.utilities            import DataInput
from fenics                       import *

# Get the Antarctica data sets
bedmap2 = DataFactory.get_bedmap2(thklim = 200)
data = bedmap2['mask']['map_data'][::-1]
db2 = DataInput(bedmap2)

# These are the original coordinates of the domain
x0 = -376234
y0 = -456870

x1 = -291856
y1 = -505791

x2 = 102477
y2 = 177085

x3 = 17833
y3 = 225849

# Convert to (lon, lat) coordinates
lon0, lat0 = db2.p(x0,y0,inverse = True)
lon1, lat1 = db2.p(x1,y1,inverse = True)
lon2, lat2 = db2.p(x2,y2,inverse = True)
lon3, lat3 = db2.p(x3,y3,inverse = True)

# Create the basemap plot
proj   = 'stere'
lat_0  = '-90'
lat_ts = '-71'
lon_0  = '0'
    
width = 3333500*2
height = 3333500*2

# This is a bit of code that I used to cut off part of the rectangular domain
# over the transantarctic mountain and the ice shelf. 

# Line that passes through (x0,y0) and (x3, y3)
def f(x) :
  m = float(y3 - y0)/float(x3 - x0)
  return m*(x - x3) + y3

# Compute two new points to define the bottom edge of the domain
x4 =-250000
y4 = f(x4)

dif_x = x3 - x4
dif_y = y3 - y4

x5 = x2 - dif_x
y5 = y2 - dif_y

out = array([[x4,y4],[x5,y5],[x2,y2],[x3,y3]])
savetxt('domain_coordinates.out',out)

# Get the (lon, lat) coordinates for the two new points
lon4, lat4 = db2.p(x4,y4,inverse = True)
lon5, lat5 = db2.p(x5,y5,inverse = True)

lons = [lon0, lon1, lon2, lon3, lon4, lon5]
lats = [lat0, lat1, lat2, lat3, lat4, lat5]

# Plot all the points
m = Basemap(width=width, height=height, resolution='h',
projection="stere", lat_ts=lat_ts, lon_0=lon_0, lat_0=lat_0)

x, y = m(lons,lats)
m.drawcoastlines(linewidth=0.25, color = 'black') 

m.scatter(x[4], y[4], 15, marker='o', color='r')
m.scatter(x[5], y[5], 15, marker='o', color='g')
m.scatter(x[2], y[2], 15, marker='o', color='b')
m.scatter(x[3], y[3], 15, marker='o', color='k')
# The two new points will be yellow
#m.scatter(x[4], y[4], 15, marker='o', color='y')
#m.scatter(x[5], y[5], 15, marker='o', color='y')
show()
