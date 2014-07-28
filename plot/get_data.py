# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 10:48:09 2014

@author: jake
"""
from varglas.data.data_factory    import DataFactory
from varglas.utilities            import DataInput
from fenics import *

# Load a mesh
mesh = Mesh('meshes/mesh_5km.xml')
#plot(mesh, interactive = True)

# create meshgrid for contour :
bedmap2 = DataFactory.get_bedmap2()
# process the data :
dbm = DataInput(bedmap2)

# Project some data onto the mesh
print "Here."
#bed = dbm.get_interpolation("B",near = True,kx=1,ky=1)

#bed = dbm.get_projection("B",near = False,kx=1,ky=1)

bed = dbm.get_spline_expression("B")
Q = FunctionSpace(mesh,'CG',1)

bed = project(bed,Q)

File('data/bed_5km.xml') << bed