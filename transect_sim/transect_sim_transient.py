from varglas.model              import Model
from varglas.solvers            import TransientSolver, SteadySolver
from varglas.physical_constants import IceParameters
from varglas.helper             import default_nonlin_solver_params
from fenics                     import *
from numpy                      import *
from scipy.interpolate          import interp1d

""" This is a simulation for the extruded transect mesh. The bed elevation is
 simply the transect extruded in the y dimension. By default, the surface
is 100 meters above the highest point in the bed and slopes upward in the -y 
direction (hence flow is in the -y direciton as well). In this case, the x axis
is across flow.

Thermo-mechanical coupling is turned on. The default surface temp. is 263K. 
Basal heat flux is initialized to a sensible value. Accumulation is 1 (m/a)
by default. Finally, Beta2 varies sinusoidally across the domain. Of course,
you can play around with all of these however you like."""

set_log_active(True)

# Directory to write results
out_dir = 'transect_results_transient/'

# Load the transect data from a file
transect_xs = loadtxt("transect_data/transect_xs.txt")
transect_zs = loadtxt("transect_data/transect_zs.txt")

# Get the range of transect xs 
xmin = transect_xs.min()
xmax = transect_xs.max()
# Also get the z range for reference
zmin = transect_zs.min()
zmax = transect_zs.max()

# Interpolate the transect data
bed = interp1d(transect_xs, transect_zs, kind = 3)

model = Model()
# Number of subdivisions for the uniform mesh
nx = 100
ny = 25
nz = 10
# The model will be about 400 km (x) across flow and 100km with flow (y)
model.generate_uniform_mesh(nx, ny, nz, xmin=xmin, xmax=xmax, ymin=0, ymax=100000, 
                            generate_pbcs=False)                          

# Expression for the bed elevation
class BedExpression(Expression):
  def eval(self, values, x):
    # Get the z coordinate for this x value
    values[0] = bed(x[0])
  
# The minimum height of the surface above the bed
min_surface = 100
# Angle of the surface slope in the y direction
alpha = 0.1 * pi / 180
# Surface slope
S = tan(alpha)

# Expression for the surface elevation
class SurfaceExpression(Expression):
  def eval(self, values, x):
    # Get the surface value at a point
    values[0] = zmax + min_surface + S*x[1]

# A sinusoidal tractiaon field
Beta2   = Expression(  '100 - 25 * sin(4*pi*x[0]/L)',
                     alpha=alpha, L=xmax)      
                     
# Deform the model geometry to the surface and bed functions
model.set_geometry(SurfaceExpression(element = model.Q.ufl_element()),
                   BedExpression(element = model.Q.ufl_element()), 
                   deform=True) 
 
# Surface mass balance expression                  
class MassBalance(Expression):
  def eval(self,values,x):
    values[0] = 1.0

SMB = MassBalance(element=model.Q.ufl_element())

# Initialize the model
model.set_parameters(IceParameters())
# The calculate boundaries function needs to know the accumulation so that it
# can initialize the boundaries properly for the age equation
model.calculate_boundaries()
model.initialize_variables()

# Good solver parameters for handling thermo-mechanical coupline
nonlin_solver_params = default_nonlin_solver_params()
nonlin_solver_params['newton_solver']['relaxation_parameter']    = 1.0
nonlin_solver_params['newton_solver']['error_on_nonconvergence'] = False
nonlin_solver_params['newton_solver']['maximum_iterations']      = 8
nonlin_solver_params['newton_solver']['absolute_tolerance']      = 1.0
nonlin_solver_params['newton_solver']['linear_solver']           = 'mumps'
nonlin_solver_params['newton_solver']['preconditioner']          = 'default'
parameters['form_compiler']['quadrature_degree']        = 2

config = { 'mode'                         : 'steady',
           'output_path'                  : out_dir,
           'wall_markers'                 : [],
           'periodic_boundary_conditions' : False,
           't_start'                      : 0.0,
           't_end'                        : 50000.0,
           'time_step'                    : 10.0,
           'log'                          : True,
           'coupled' : 
           { 
             'on'                  : True,
             'inner_tol'           : 0.0,
             'max_iter'            : 1
           },
           'velocity' : 
           { 
             'on'                         : True,
             'newton_params'              : nonlin_solver_params,
             'viscosity_mode'             : 'full',
             'b_linear'                   : None,
             'use_T0'                     : True,
             'T0'                         : 263.0,
             'A0'                         : 1e-16,
             'beta2'                      : 25,
             'r'                          : 1.0,
             'E'                          : 1.0,
             'approximation'              : 'fo',
             'boundaries'                 : None,
             'log'                        : True,
             'init_beta_from_U_ob'        : False
           },
           'enthalpy' : 
           { 
             'on'                  : True,
             'use_surface_climate' : False,
             'T_surface'           : 263.0,
             'q_geo'               : 0.00042*60**2*24*365,
             'lateral_boundaries'  : None,
             'log'                 : True
           },
           'free_surface' :
           { 
             'on'                         : True,
             'lump_mass_matrix'           : False,
             'use_shock_capturing'        : False,
             'thklim'                     : None,
             'use_pdd'                    : False,
             'observed_smb'               : SMB,
             'static_boundary_conditions' : False
           },  
           'age' : 
           { 
             'on'                  : False,
             'use_smb_for_ela'     : False,
             'ela'                 : None
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
           
F = SteadySolver(model, config)
F.solve()
 
T = TransientSolver(model, config)
T.solve()

File(out_dir + 'beta2.pvd') << interpolate(model.beta2, model.Q)


