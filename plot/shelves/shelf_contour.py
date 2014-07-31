"""
Create contours for the shelves so we can plot them. 
"""

from pylab import *
from varglas.data.data_factory import DataFactory
from varglas.utilities import DataInput, MeshGenerator
from numpy import *

# Get the Antarctica data sets
bedmap2 = DataFactory.get_bedmap2()

# Create a countour of the continent - without the ice shelves
db2 = DataInput(bedmap2)
db2.set_data_val('mask',127,0)

mg = MeshGenerator(db2, 'mesh', '')
mg.create_contour('mask', 0, skip_pts=4)
mg.eliminate_intersections(dist=40)
# Get the longest contour, which will be the coastline 
#cont = mg.longest_cont

# Get the biggest contours
cl = mg.c.allsegs[0]
bigest_contours = array(map(len, cl))
bigest_contours.argsort()
print(bigest_contours.sort())

print(bigest_contours,bigest_contours.min(),bigest_contours.max())

print(len(cl[bigest_contours[0]]))
print(len(cl[bigest_contours[1]]))
#plot(cont[:,0], cont[:,1])
#show()