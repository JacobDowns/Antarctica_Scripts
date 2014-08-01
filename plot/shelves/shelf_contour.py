"""
Create contours for the Antarctic ice shelves so we can plot them. 
"""

from pylab import *
from varglas.data.data_factory import DataFactory
from varglas.utilities import DataInput, MeshGenerator
from numpy import *

# Get the Antarctica data sets
bedmap2 = DataFactory.get_bedmap2()
db2 = DataInput(bedmap2)
# Just get the ice shelves
db2.set_data_val('mask',127,0)

mg = MeshGenerator(db2, 'mesh', '')
mg.create_contour('mask', 0, skip_pts=2)
mg.eliminate_intersections(dist=20)

# Get the two longest contours, which I'm assuming are the two major ice shelves
cl = mg.c.allsegs[0]
contour_lens = array(map(len, cl))
sorted_indexes = contour_lens.argsort()

shelf1 = cl[sorted_indexes[-1]]
shelf2 = cl[sorted_indexes[-2]]

# Convert to (lon, lat coordinates)
shelf1_lons, shelf1_lats = db2.p(shelf1[:,0], shelf1[:,1], inverse = True)
shelf2_lons, shelf2_lats = db2.p(shelf2[:,0], shelf2[:,1], inverse = True)

# Save the ice shelf contours
savetxt('shelf1_cont.out', array(zip(shelf1_lons, shelf1_lats)))
savetxt('shelf2_cont.out', array(zip(shelf2_lons, shelf2_lats)))