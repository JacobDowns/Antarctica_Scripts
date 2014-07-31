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
out_dir = 'results_stokes/'

set_log_active(True)
#parameters["allow_extrapolation"] = True

mesh = Mesh('data/meshes/ant_mesh.xml')

# Get a bunch of data to use in the simulation 
thklim = 100.0
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

# Setup the model
model = model.Model()
model.set_mesh(mesh)
model.set_geometry(S, B, deform=True)

# Load the velocities for the boundaries
u = Function(model.Q)
v = Function(model.Q)
w = Function(model.Q)
File("data/boundary_velocity/u_bound.xml") >> u
File("data/boundary_velocity/v_bound.xml") >> v
File("data/boundary_velocity/w_bound.xml") >> w

model.set_parameters(pc.IceParameters())
model.calculate_boundaries(adot = adot)
model.initialize_variables()

# Specifify non-linear solver parameters :
nonlin_solver_params = default_nonlin_solver_params()
nonlin_solver_params['newton_solver']['relaxation_parameter']    = 0.7
nonlin_solver_params['newton_solver']['relative_tolerance']      = 1e-3
nonlin_solver_params['newton_solver']['maximum_iterations']      = 15
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
             'beta'                : 4,
             'init_beta_from_U_ob' : False,
             'boundaries'          : 'user_defined',
             'u_lat_boundary' : u,
             'v_lat_boundary' : v,
             'w_lat_boundary' : w,
             'r'                   : 1.0,
             'E'                   : 1.0,
             'approximation'       : 'stokes',
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
