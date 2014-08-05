# -*- coding: utf-8 -*-
"""
Create a uniform mesh of Antarctica for plotting. 
"""

from varglas.utilities         import DataInput, MeshGenerator
from varglas.data.data_factory import DataFactory
from pylab                     import *

thklim = 0
# create meshgrid for contour :
bedmap2 = DataFactory.get_bedmap2()
# process the data :
dbm = DataInput(bedmap2, gen_space=False)
dbm.set_data_val("H", 32767, thklim)

m = MeshGenerator(dbm, 'mesh', '')

m.create_contour('H', 0.0, 5)
m.eliminate_intersections(dist=20)

m.write_gmsh_contour(1000, boundary_extend=False)
m.add_edge_attractor(1)

#field, ifield, lcMin, lcMax, distMin, distMax
m.add_threshold(2, 1, 3000, 3000, 1, 100000)
m.finish(4)

#m.create_2D_mesh('mesh') #FIXME: fails
#m.convert_msh_to_xml('mesh', 'mesh')