import varglas.solvers            as solvers
import varglas.physical_constants as pc
from varglas.data.data_factory    import DataFactory
from varglas.helper               import default_nonlin_solver_params
from varglas.utilities            import DataInput
from fenics                       import *
import varglas.model              as model

# Output directory
out_dir = 'results/'

set_log_active(True)

thklim = 100

measures  = DataFactory.get_ant_measures(res=900)
bedmap1   = DataFactory.get_bedmap1(thklim=thklim)
bedmap2   = DataFactory.get_bedmap2(thklim=thklim)

mesh = Mesh('meshes/realistic_mesh.xml')

dm  = DataInput(measures, mesh=mesh)
db1 = DataInput(bedmap1,  mesh=mesh)
db2 = DataInput(bedmap2,  mesh=mesh)

H      = db2.get_nearest_expression("H")
S      = db2.get_nearest_expression("S")
B      = db2.get_nearest_expression("B")
T_s    = db1.get_nearest_expression("srfTemp")
q_geo  = db1.get_nearest_expression("q_geo")
adot   = db1.get_nearest_expression("adot")

model = model.Model()
model.set_mesh(mesh)
model.set_geometry(S, B,deform=True)
model.set_parameters(pc.IceParameters())
model.calculate_boundaries()
model.initialize_variables()

# Load in the velocity data
#u = Function(model.Q)
#v = Function(model.Q)
#w = Function(model.Q)

File("velocity_data/u.xml") >> u
File("velocity_data/v.xml") >> v
File("velocity_data/w.xml") >> w

plot(u, interactive = True)

quit()

# specifify non-linear solver parameters :
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
             'beta2'               : 4,
             'init_beta_from_U_ob' : False,
             'r'                   : 1.0,
             'E'                   : 1.0,
             'approximation'       : 'fo',
             'boundaries'          : None,
             'log'                 : True
           },
           'enthalpy' : 
           { 
             'on'                  : True,
             'use_surface_climate' : False,
             'T_surface'           : T_s,
             'q_geo'               : q_geo,
             'lateral_boundaries'  : None,
             'log'                 : False
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
             'on'                  : False,
             'use_smb_for_ela'     : True,
             'ela'                 : 750,
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
#File(out_dir + 'beta_0.pvd') << model.beta2
F.solve()



