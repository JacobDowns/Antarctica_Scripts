from varglas.model              import Model
from varglas.solvers            import SteadySolver
from varglas.physical_constants import IceParameters
from varglas.helper             import default_nonlin_solver_params
from fenics                     import set_log_active, File, Expression, interpolate
from numpy                      import *
from scipy.interpolate          import interp1d
set_log_active(True)

# Directory to write results
out_dir = 'transect_results/'

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
nx = 250
ny = 30
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
# Slope of surface
S = tan(alpha)

# Expression for the surface elevation
class SurfaceExpression(Expression):
  def eval(self, values, x):
    # Get the surface value at a point
    values[0] = zmax + min_surface + S*x[1]

# Sinusoidal traction field
Beta2   = Expression(  '100 - 80 * sin(4*pi*x[0]/L)',
                     alpha=alpha, L=xmax)
                     
# Accumulation is 1 (m/a)  
adot = Constant(1.0)     
  
# Deform the model geometry to the surface and bed functions
model.set_geometry(SurfaceExpression(element = model.Q.ufl_element()),
                   BedExpression(element = model.Q.ufl_element()), 
                   deform=True)
                   
model.set_parameters(IceParameters())
# The calculate boundaries function needs to know the accumulation so that it
# can initialize the boundaries properly for the age equation
model.calculate_boundaries(adot = adot)
model.initialize_variables()

nonlin_solver_params = default_nonlin_solver_params()
nonlin_solver_params['newton_solver']['linear_solver']  = 'gmres'
nonlin_solver_params['newton_solver']['preconditioner'] = 'hypre_amg'

config = { 'mode'                         : 'steady',
           'output_path'                  : out_dir,
           'wall_markers'                 : [],
           'periodic_boundary_conditions' : False,
           't_start'                      : None,
           't_end'                        : None,
           'time_step'                    : None,
           'log'                          : True,
           'coupled' : 
           { 
             'on'                  : False,
             'inner_tol'           : 0.0,
             'max_iter'            : 1
           },
           'velocity' : 
           { 
             'on'                  : True,
             'newton_params'       : nonlin_solver_params,
             'viscosity_mode'      : 'isothermal',
             'b_linear'            : None,
             'use_T0'              : False,
             'T0'                  : None,
             'A0'                  : 1e-16,
             'beta2'               : Beta2,
             'r'                   : 0.0,
             'E'                   : 1,
             'approximation'       : 'fo',
             'boundaries'          : None,
             'log'                 : True,
             'init_beta_from_U_ob' : False
           },
           'enthalpy' : 
           { 
             'on'                  : False,
             'use_surface_climate' : False,
             'T_surface'           : None,
           },
           'free_surface' :
           { 
             'on'                  : False,
             'thklim'              : None,
             'use_pdd'             : False,
             'observed_smb'        : 1.0,
           },  
           'age' : 
           { 
             'on'                  : False,
             'use_smb_for_ela'     : False,
             'ela'                 : None,
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

File(out_dir + 'beta2.pvd') << interpolate(Beta2, model.Q)



