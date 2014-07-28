# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 09:45:31 2014

@author: jake
"""
from numpy import *
from scipy.interpolate import interp1d
from varglas.data.data_factory import DataFactory
from varglas.utilities import DataInput, MeshRefiner, MeshGenerator
import varglas.model as model
from fenics import *


# First create a flat mesh, unstructured mesh

# Load the transect data from a file
transect_xs = loadtxt("transect_data/transect_xs.txt")
transect_zs = loadtxt("transect_data/transect_zs.txt")

# Interpolate the transect bed data
bed_spline = interp1d(transect_xs, transect_zs, kind = 3)

# Use the data to get the extent of the domain
xmin = transect_xs.min()
xmax = transect_xs.max()
# Get the maximum bed elevation
zmax = transect_zs.max()

cont = array([
  [xmin, 0],
  [xmax, 0],
  [xmax, 100000],
  [xmin, 100000]
])

# Name of refined mesh
mesh_name = 'transect_mesh'

# Get the Antarctica data sets
bedmap2   = DataFactory.get_bedmap2(thklim=200)
# Load in a DataInput object. We won't use it, but we need to pass a DataInput
# to the MeshGenerator, and we have to fake it out.
db2 = DataInput(None, bedmap2)

# Create a mesh file in the current directory 
m = MeshGenerator(db2, mesh_name, '')
# Manually set the countour instead of calculating it automatically
m.set_contour(cont)
# Write the contour points to the mesh file
m.write_gmsh_contour(100000, boundary_extend = False)
# Extrude the flat mesh 10,000 meters in the z dimension. The height of the 
# mesh can be automatically scaled to the proper height by the model object
m.extrude(20000, 10)

# We're finished with the flat mesh!
m.close_file()

# Refine the mesh based on thickness

# Wrap the bed spline in a function that takes two arguments
def bed(x,y) :
  return bed_spline(x)

# Define a function for getting the surface elevation

# The minimum height of the surface above the bed
min_surface = 200
# Angle of the surface slope in the y direction
alpha = 0.1 * pi / 180
# Surface slope
S = tan(alpha)

# Expression for the surface elevation
def surface(x,y):
  # Get the surface value at a point
  #return zmax + min_surface
  return zmax + min_surface + S*y
    
# Function that calculates the height 
def H(x,y) :
  H = surface(x,y) - bed(x,y)
  return array([[H]])
  
# Refine the mesh based on thickenss
ref_bm = MeshRefiner(db2, 'H', gmsh_file_name = mesh_name) 
ref_bm.spline = H

# Refine the mesh based on the refinement radius
a, aid = ref_bm.add_static_attractor(1)
ref_bm.set_background_field(aid)
# Write out the file
ref_bm.finish(gui=False, out_file_name = mesh_name)

# Convert the generated .msh file to an xml file
m.convert_msh_to_xml(mesh_name, mesh_name)

# Now deform the refined mesh to match the surface and bed velocity
refined_mesh = Mesh(mesh_name + ".xml")

# Expression for the bed elevation
class BedExpression(Expression):
  def eval(self, values, x):
    # Get the z coordinate for this x value
    values[0] = bed(x[0],x[1])

# Expression for the surface elevation
class SurfaceExpression(Expression):
  def eval(self, values, x):
    # Get the surface value at a point
    #values[0] = surface(x[0],x[1])
    values[0] = surface(x[0],x[1])

model = model.Model()
# Set the mesh to the non-deformed anisotropic mesh
model.set_mesh(refined_mesh)

# Deform it to match the surface and bed geometry
model.set_geometry(SurfaceExpression(element = model.Q.ufl_element()), BedExpression(element = model.Q.ufl_element()), deform = False)
model.deform_mesh_to_geometry()

plot(model.mesh, interactive = True)
# Save the mesh
File(mesh_name + '_deformed.xml') << model.mesh
File(mesh_name + '_deformed.pvd') << model.mesh

print(len(model.mesh.coordinates()[:]))
