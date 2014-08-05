"""
Create a grounding line contour.
"""

from varglas.data.data_factory import DataFactory
from varglas.utilities import DataInput, MeshGenerator
from numpy import *

# Get the Antarctica data sets
bedmap2 = DataFactory.get_bedmap2()
db2 = DataInput(bedmap2)
# Get the grounding line by eliminating the shelves
db2.set_data_val('mask',1,127)

# Create a grounding line countour
mg = MeshGenerator(db2, 'mesh', '')
mg.create_contour('mask', 10, skip_pts=4)
mg.eliminate_intersections(dist=20)
cont = mg.longest_cont

# Convert (x,y) coordinates to (lon,lat)
cont_lons, cont_lats = db2.p(cont[:,0], cont[:,1], inverse = True)

# Save the contour
savetxt('grounding_cont.out', array(zip(cont_lons, cont_lats)))