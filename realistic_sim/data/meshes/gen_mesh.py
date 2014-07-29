""" This scripts builds a flat mesh for a rectangular region in Antarctica and 
refines it based on thickness. """

from varglas.data.data_factory import DataFactory
from varglas.utilities import DataInput, MeshGenerator, MeshRefiner
from fenics import *
from numpy import *
from pylab import *

thklm = 200.0
bm2 = DataFactory.get_bedmap2(thklm)
bedmap2 = DataInput(bm2)

# Load the domain coordinates
domain_coordinates = loadtxt('../domain_coordinates.out')

mesh_name = 'ant_mesh'

# Create a contour for the domain
#=======================================================
# Create a mesh file in the current directory 
m = MeshGenerator(bedmap2, mesh_name, '')
# Manually set the countour instead of calculating it automatically
m.set_contour(domain_coordinates)
# Write the contour points to the mesh file
m.write_gmsh_contour(100000, boundary_extend = False)
# Extrude the flat mesh 10,000 meters in the z dimension. The height of the 
# mesh can be automatically scaled to the proper height by the model object
m.extrude(10000, 10)
# We're finished with the flat mesh!
m.close_file()


# Refine the mesh based on ice thickness
#=======================================================
ref_bm = MeshRefiner(bedmap2, 'H', gmsh_file_name = mesh_name) 
# Refine the mesh based on the refinement radius
a, aid = ref_bm.add_static_attractor(2)
ref_bm.set_background_field(aid)
# Write out the file
ref_bm.finish(gui=False, out_file_name = mesh_name)
  
# Convert the generated .msh file to an xml file
m.convert_msh_to_xml(mesh_name, mesh_name)
