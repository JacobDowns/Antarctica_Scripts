"""
Create a grounding line contour.
"""

from varglas.data.data_factory import DataFactory
from varglas.utilities import DataInput, MeshGenerator
from numpy import *
from mpl_toolkits.basemap import Basemap

# Get the Antarctica data sets
bedmap2 = DataFactory.get_bedmap2()
db2 = DataInput(bedmap2)

# Get the grounding line by eliminating the shelves
db2.set_data_val('mask',1,127)

# Create a grounding line countour
mg = MeshGenerator(db2, 'mesh', '')
mg.create_contour('mask', 10, skip_pts=2)
mg.eliminate_intersections(dist=20)
cont = mg.longest_cont

# Convert (x,y) coordinates to (lon,lat)
cont_lons, cont_lats = db2.p(cont[:,0], cont[:,1], inverse = True)

# Convert (x,y) coordinates to (lon,lat)
cont_lons, cont_lats = db2.p(cont[:,0], cont[:,1], inverse = True)

# Convert to basemap coordinates
lat_0  = '-90'
lat_ts = '-71'
lon_0  = '0'
height = 3333500*2
width = 3333500*2

m = Basemap(width=width, height=height, resolution='h',
            projection="stere", lat_ts=lat_ts, lon_0=lon_0, lat_0=lat_0)

cont_xs, cont_ys = m(cont_lons, cont_lats)

# Save the contour
savetxt('../data/grounding_basemap.out', array(zip(cont_xs, cont_ys)))