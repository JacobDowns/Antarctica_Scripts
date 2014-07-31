""" Somehow figure out how to group the glaciers...
"""

from pylab import *
from varglas.data.data_factory import DataFactory
from varglas.utilities import DataInput, MeshGenerator
from numpy import *

# Get the Antarctica data sets
bedmap2 = DataFactory.get_bedmap2(thklim = 200)

# Create a countour of the continent - without the ice shelves
db2 = DataInput(bedmap2)
db2.set_data_val('mask',1,127)
mg = MeshGenerator(db2, 'mesh', '')
mg.create_contour('mask', 0, skip_pts=2)
mg.eliminate_intersections(dist=40)
# Get the longest contour, which will be the coastline 
cont = mg.longest_cont


plot(cont[:,0], cont[:,1] ,'ro', ms = 5)
show()
print(cont[:,0].min(),cont[:,1].max())

# Convert contour coordinates to (lon, lat coordinates)
lon_cont, lat_cont = db2.p(cont[:,0],cont[:,1], inverse = True)
# Write out the contour data
cont_data = array(zip(lon_cont,lat_cont))
cont_data = savetxt('cont.out',cont_data)


quit()

#print(len(cont))
#quit()

# Load the glacier data
glacier_data = loadtxt('outlet_glaciers.out', delimiter = '|', dtype = 'str')
names = array(glacier_data[:,0], dtype = 'str')
lons = array(glacier_data[:,1], dtype = 'f')
lats = array(glacier_data[:,2], dtype = 'f')

# Convert lons and lats to x, y coordinates
x, y = db2.p(lons, lats)

# Plot the outlet glaciers
plot(x, y ,'ro', ms = 5)
show()