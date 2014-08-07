""" Run a simulation on the rectangular Antarctic domain using bedmap2 for
surface and bed elevation. """

import varglas.solvers            as solvers
import varglas.physical_constants as pc
from varglas.data.data_factory    import DataFactory
from varglas.helper               import default_nonlin_solver_params
from varglas.utilities            import DataInput
from fenics                       import *
import varglas.model              as model

# Output directory
out_dir = 'age_bp/'

set_log_active(True)

# Load my mesh
mesh = Mesh('data/meshes/ant_mesh.xml')

# Get a bunch of data to use in the simulation 
thklim = 100.0
bedmap1   = DataFactory.get_bedmap1(thklim=thklim)
bedmap2   = DataFactory.get_bedmap2(thklim=thklim)

db1 = DataInput(bedmap1,  mesh=mesh)
db2 = DataInput(bedmap2,  mesh=mesh)

# This code is 
db2.data['B'] = db2.data['S'] - db2.data['H']
db2.set_data_val('H', 32767, thklim)
db2.data['S'] = db2.data['B'] + db2.data['H']

S      = db2.get_spline_expression("S")
B      = db2.get_spline_expression("B")
adot   = db1.get_spline_expression("adot")

# Setup the model
model = model.Model()
model.set_mesh(mesh)
model.set_geometry(S, B, deform=True)
model.set_parameters(pc.IceParameters())
model.calculate_boundaries(adot = adot)
model.initialize_variables()

# Load the bp velocity fields
u = Function(model.Q)
v = Function(model.Q)
w = Function(model.Q)
File('results_bp/u.xml') >> u
File('results_bp/v.xml') >> v
File('results_bp/w.xml') >> w
model.u = u
model.v = v
model.w = w

# Load the initial age
age = Function(model.Q)
File("data/projected_data/age.xml") >> age
# Set the starting age of the model
model.A = age

config = { 'mode'                         : 'transient',
           't_start'                      : 0,
           't_end'                        : 1000,
           'time_step'                    : 10,
           'output_path'                  : out_dir,
           'wall_markers'                 : [],
           'periodic_boundary_conditions' : False,
           'log'                          : False,
           'coupled' : 
           { 
             'on'                  : False,
             'inner_tol'           : 0.0,
             'max_iter'            : 1
           },
           'velocity' : 
           { 
             'on'                  : False,
             'newton_params'       : None,
             'viscosity_mode'      : 'full',
             'b_linear'            : None,
             'use_T0'              : True,
             'T0'                  : 263,
             'A0'                  : 1e-16,
             'beta'                : None,
             'init_beta_from_U_ob' : False,
             'boundaries'          : None,
             'r'                   : 0.0,
             'E'                   : 1.0,
             'approximation'       : 'fo',
             'log'                 : True
           },
           'enthalpy' : 
           { 
             'on'                  : False,
             'use_surface_climate' : False,
             'T_surface'           : None,
             'q_geo'               : None,
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
             'log'                 : True
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

T = solvers.TransientSolver(model, config)
T.solve()


