""" This script projects Evan's data onto my mesh so that it can be used
in my realistic Antarctica simulation. """

from varglas.data.data_factory    import DataFactory
from varglas.mesh.mesh_factory    import MeshFactory
from varglas.utilities            import DataInput
from fenics                       import *
import varglas.model              as model

# Have to set this to true because my mesh doesn't match up with Evan's pefectly
# due to different levels of refinement
parameters["allow_extrapolation"] = True

# Load my mesh
mesh = Mesh('meshes/ant_mesh.xml')

# Use bedmap for surface and bed elevation
thklim = 100.0
bedmap2   = DataFactory.get_bedmap2(thklim=thklim)
db2 = DataInput(bedmap2, mesh = mesh)

# Deform the mesh so it matches Evan's
db2.data['B'] = db2.data['S'] - db2.data['H']
db2.set_data_val('H', 32767, thklim)
db2.data['S'] = db2.data['B'] + db2.data['H']

S = db2.get_spline_expression("S")
B = db2.get_spline_expression("B")

# Create a model for the sole purpose of deforming the full continent mesh
full_mesh = MeshFactory.get_antarctica_3D_gradS_detailed()
mesh_model = model.Model()
mesh_model.set_mesh(full_mesh)
mesh_model.set_geometry(S, B, deform=True)

# Project the velocity fields onto the deformed, full continent mesh
# Load in the velocity data
u = Function(mesh_model.Q)
v = Function(mesh_model.Q)
w = Function(mesh_model.Q)
File("evan_data/u.xml") >> u
File("evan_data/v.xml") >> v
File("evan_data/w.xml") >> w

# "Convert" the full continent velocity expressions to expressions
class UExpression(Expression):
  def eval(self, values, x):
    values[0] = u(x)
    
class VExpression(Expression):
  def eval(self, values, x):
    values[0] = v(x)
    
class WExpression(Expression):
  def eval(self, values, x):
    values[0] = w(x)

# Setup another model for the purpose of deforming my mesh
model = model.Model()
model.set_mesh(mesh)
model.set_geometry(S, B, deform=True)

# Now project the velocity expressions onto my mesh
u_out = project(UExpression(), model.Q)
v_out = project(VExpression(), model.Q)
w_out = project(WExpression(), model.Q)
File('boundary_velocity/u_bound.xml') << u_out
File('boundary_velocity/v_bound.xml') << v_out
File('boundary_velocity/w_bound.xml') << w_out

# Project beta onto my mesh
beta = Function(mesh_model.Q)
File("evan_data/beta.xml") >> beta

# "Convert" beta field to an expression
class BetaExpression(Expression):
  def eval(self, values, x):
    values[0] = beta(x)
    
# Now project beta on my mesh and write it out
beta_out = project(BetaExpression(), model.Q)
File('projected_data/beta.xml') << beta_out
File('projected_data/beta.pvd') << beta_out

# Project age onto my mesh
age = Function(mesh_model.Q)
File("evan_data/age.xml") >> age

class AgeExpression(Expression):
  def eval(self, values, x):
    values[0] = age(x)

age_out = project(AgeExpression(), model.Q)
File('projected_data/age.xml') << age_out
File('projected_data/age.pvd') << age_out
