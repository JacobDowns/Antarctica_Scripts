# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 16:12:36 2014

@author: jake
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
mg.create_contour('mask', 0, skip_pts=4)
mg.eliminate_intersections(dist=40)
# Get the longest contour, which will be the coastline 
cont = mg.longest_cont

# Load the glacier data
glacier_data = loadtxt('glacier_data.out', delimiter = '|', dtype = 'str')
names = array(glacier_data[:,0], dtype = 'str')
lons = array(glacier_data[:,1], dtype = 'f')
lats = array(glacier_data[:,2], dtype = 'f')

# Convert lons and lats to x, y coordinates
x, y = db2.p(lons,lats)

# Next, eliminate glaciers that are too far from the coast

# (x,y) coordinates of outlet glaciers for plotting
x_out = []
y_out = []

# The names, and (lon, lat) coordinates of the outlet glaciers, which we'll save
# to a file
names_out = []
lon_out = []
lat_out = []

for i in range(len(x)) :
  v = [x[i], y[i]]
  # Compute distance from all points in the countour : not very efficient, but
  # oh well
  min_dist = array(map(lambda x : linalg.norm(v - x), cont)).min()
  
  if min_dist < 2800 :
    x_out.append(x[i])
    y_out.append(y[i])
    
    names_out.append(names[i])
    lon_out.append(lons[i])
    lat_out.append(lats[i])

print(len(names_out))

# Save the outlet glacier data
outlet_data = array(zip(names_out, lon_out, lat_out))
savetxt('outlet_glaciers.out', outlet_data, delimiter = '|',  fmt="%s")

# Plot the outlet glaciers
plot(x, y, 'ko', ms = 3)
plot(x_out,y_out,'ro',ms = 5)
show()