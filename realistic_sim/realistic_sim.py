""" Run a simulation on the Antarctic domain with realistic surface and bed
elevation. """

import varglas.solvers            as solvers
import varglas.physical_constants as pc
from varglas.data.data_factory    import DataFactory
from varglas.mesh.mesh_factory    import MeshFactory
from varglas.helper               import default_nonlin_solver_params
from varglas.utilities            import DataInput
from fenics                       import *
import varglas.model              as model

# Output directory
out_dir = 'results/'

set_log_active(True)

mesh = Mesh('data/meshes/ant_mesh.xml')

# Get a bunch of data to use in the simulation 
thklim = 100
measures  = DataFactory.get_ant_measures(res=900)
bedmap1   = DataFactory.get_bedmap1(thklim=thklim)
bedmap2   = DataFactory.get_bedmap2(thklim=thklim)

dm  = DataInput(measures, mesh=mesh)
db1 = DataInput(bedmap1,  mesh=mesh)
db2 = DataInput(bedmap2,  mesh=mesh)

# Fix some stuff?
db2.data['B'] = db2.data['S'] - db2.data['H']
db2.set_data_val('H', 32767, thklim)
db2.data['S'] = db2.data['B'] + db2.data['H']

S      = db2.get_spline_expression("S")
B      = db2.get_spline_expression("B")
T_s    = db1.get_spline_expression("srfTemp")
q_geo  = db1.get_spline_expression("q_geo")
adot   = db1.get_spline_expression("adot")

# Create a model for the sole purpose of deforming the full continent mesh
# Get the full continent mesh
full_mesh = MeshFactory.get_antarctica_3D_gradS_detailed()
mesh_model = model.Model()
mesh_model.set_mesh(full_mesh)
mesh_model.set_geometry(S, B, deform=True)

# Project the velocity fields onto the deformed, full continent mesh
# Load in the velocity data
u = Function(mesh_model.Q)
v = Function(mesh_model.Q)
w = Function(mesh_model.Q)
File("data/u.xml") >> u
File("data/v.xml") >> v
File("data/w.xml") >> w

# Create some expressions from the velocity functions
class UExpression(Expression):
  def eval(self, values, x):
    try :
      values[0] = u(x)
    except :
      pass
    
class VExpression(Expression):
  def eval(self, values, x):
    try :
      values[0] = v(x)
    except :
      pass
    
class WExpression(Expression):
  def eval(self, values, x):
    try :    
      values[0] = u(x)
    except :
      pass

# Setup the model
model = model.Model()
model.set_mesh(mesh)
model.set_geometry(S, B, deform=True)

# Apparently the smb is only used in the transient solver with free-surface  
# so adot isn't projected onto the mesh otherwise by the steady solver.
# In order to view adot in paraview, I'll just output it manually
adot_out = project(adot,model.Q)
File(out_dir + '/adot.pvd') << adot_out

model.set_parameters(pc.IceParameters())
model.calculate_boundaries(adot = adot)
model.initialize_variables()

# Specifify non-linear solver parameters :
nonlin_solver_params = default_nonlin_solver_params()
nonlin_solver_params['newton_solver']['relaxation_parameter']    = 0.7
nonlin_solver_params['newton_solver']['relative_tolerance']      = 1e-3
nonlin_solver_params['newton_solver']['maximum_iterations']      = 10
nonlin_solver_params['newton_solver']['error_on_nonconvergence'] = False
nonlin_solver_params['newton_solver']['linear_solver']           = 'mumps'
nonlin_solver_params['newton_solver']['preconditioner']          = 'default'
parameters['form_compiler']['quadrature_degree']                 = 2

config = { 'mode'                         : 'steady',
           't_start'                      : None,
           't_end'                        : None,
           'time_step'                    : None,
           'output_path'                  : out_dir,
           'wall_markers'                 : [],
           'periodic_boundary_conditions' : False,
           'log'                          : True,
           'coupled' : 
           { 
             'on'                  : True,
             'inner_tol'           : 0.0,
             'max_iter'            : 1
           },
           'velocity' : 
           { 
             'on'                  : True,
             'newton_params'       : nonlin_solver_params,
             'viscosity_mode'      : 'full',
             'b_linear'            : None,
             'use_T0'              : True,
             'T0'                  : 263,
             'A0'                  : 1e-16,
             'beta'               : 2,
             'init_beta_from_U_ob' : False,
             'boundaries'          : 'user_defined',
             'u_lat_boundary' : UExpression(),
             'v_lat_boundary' : VExpression(),
             'w_lat_boundary' : WExpression(),
             'r'                   : 1.0,
             'E'                   : 1.0,
             'approximation'       : 'fo',
             'log'                 : True
           },
           'enthalpy' : 
           { 
             'on'                  : True,
             'use_surface_climate' : False,
             'T_surface'           : T_s,
             'q_geo'               : q_geo,
             'lateral_boundaries'  : None,
             'log'                 : True
           },
           'free_surface' :
           { 
             'on'                  : False,
             'lump_mass_matrix'    : True,
             'thklim'              : None,
             'use_pdd'             : False,
             'observed_smb'        : adot,
           },  
           'age' : 
           { 
             'on'                  : True,
             'use_smb_for_ela'     : True,
             'ela'                 : None,
             # Use the facet function to apply the 
             'use_ff_for_ela'      : False
           },
           'surface_climate' : 
           { 
             'on'                  : False,
             'T_ma'                : None,
             'T_ju'                : None,
             'beta_w'              : None,
             'sigma'               : None,
             'precip'              : None
           },
           'adjoint' :             
           {                       
             'alpha'               : None,
             'beta'                : None,
             'max_fun'             : None,
             'objective_function'  : 'logarithmic',
             'animate'             : False
           }}

F = solvers.SteadySolver(model, config)
F.solve()

# Output some additional fields
File(out_dir + '/qgeo.pvd') << model.q_geo




