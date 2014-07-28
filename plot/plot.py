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

x0 = -376234
y0 = -456870

x1 = -291856
y1 = -505791

x2 = 102477
y2 = 177085

x3 = 17833
y3 = 225849

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

"""lon0, lat0 = (-139.72716740712372, -84.37814266271583)
lon1, lat1 = (-151.11913845599102, -84.38752263197189)
lon2, lat2 = (32.57932373223234, -88.02904611869094)
lon3, lat3 = (2.0840591368348487, -87.75539881594261)"""


lon4 = 66.46
lat4 = 64.31

lons = [lon0, lon1, lon2, lon3]
lats = [lat0, lat1, lat2, lat3]

print(lons)
print(lats)

m = Basemap(width=width, height=height, resolution='h',
projection="stere", lat_ts=lat_ts, lon_0=lon_0, lat_0=lat_0)

#xs = [x0, x1, x2, x3]
#ys = [y0, y1, y2, y3]
x, y = m(lons,lats)

m.drawcoastlines(linewidth=0.25, color = 'black') 

m.scatter(x, y, 3, marker='o', color='r')
show()
