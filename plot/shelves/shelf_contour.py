"""
Create contours for the Antarctic ice shelves so we can plot them. 
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

# Get the two longest contours, which I'm assuming are the two major ice shelves
cl = mg.c.allsegs[0]
contour_lens = array(map(len, cl))
sorted_indexes = contour_lens.argsort()

shelf1 = cl[sorted_indexes[-1]]
shelf2 = cl[sorted_indexes[-2]]

# Save the ice shelves
savetxt('shelf1_cont.out', shelf1)
savetxt('shelf2_cont.out', shelf2)
