"""
Plot of Antarctica bed data.
"""

from mpl_toolkits.basemap import Basemap
from pylab import *
import numpy as numpy
from matplotlib import cm
from varglas.data.data_factory import DataFactory
from varglas.utilities import DataInput
from fenics import *
from matplotlib import colors
import custom_cmaps

rc('font',**{'size'   : 22})
#rc('text', usetex=True)

class AntarcticaPlot :
    
  def __init__(self,u) :
    # Get the mesh data
    mesh  = u.function_space().mesh()
    coords = mesh.coordinates()
    # Get the triangular cells from the mesh
    self.tri_cells = mesh.cells()
    
    # Create a vector to hold the vertex values. Fenics apparently expects a numpy
    # array the same length as u.vector()
    self.v = numpy.zeros(len(u.vector().array()),dtype='d')
    self.v = u.compute_vertex_values(mesh)
    
    print(self.v.min(), self.v.max())

    # Replace any values outside of the range of the color map, assuming each 
    # color spans 200 meters
    self.v[self.v < -5000] = -5000
    self.v[self.v > 3600] = 3600
    
    # x and y coordinates of mesh vertices
    vxs = coords[:,0]
    vys = coords[:,1]
    
    # Create a data input object from the bedmap 2 data so that we can get its
    # projection object
    bedmap2 = DataFactory.get_bedmap2()
    dbm = DataInput(bedmap2)
    
    # Get lon,lat coordinates of the mesh vertices
    self.v_lons,self.v_lats = dbm.p(vxs,vys,inverse=True)
  
  # Draw the outline of Greenland and the meridians
  def plot(self) :
    print("Plotting...")
    self.fig = plt.figure(figsize=(24,27))
    self.ax = self.fig.add_axes()
    
    plt.title("Antarctica Bedrock Elevation", {'fontsize':52}, y = 1.04)
     
    # Projection params
    lat_0  = '-90'
    lat_ts = '-71'
    lon_0  = '0'
    # Height and width of the projection
    height = 3333500*2
    width = 3333500*2
    #height = 3633500*2
    #width = 3633500*2
    
    # Create the basemap plot
    self.m = Basemap(ax=self.ax, width=width, height=height, resolution='f',
    projection="stere", lat_ts=lat_ts, lon_0=lon_0, lat_0=lat_0)
     
    # Draw coastlines
    #self.m.drawcoastlines(linewidth=0.25, color = 'black')
    
    self.plot_meridians()        
    self.plot_grounding_line()
    self.plot_continent()
    self.plot_data()
    savefig('bed1.png',dpi = 350)
    #show()
  
  # Plots the data
  def plot_data(self) :
    # Convert lat and lon coordinates for mesh vertices to x and y 
    # map coordinates
    x, y = self.m(self.v_lons,self.v_lats)     
    
    # Upper and lower range of the data
    #bounds = arange(-5400,3600+200,200)
    bounds = linspace(-5000,3600,44)
    norm = colors.BoundaryNorm(bounds, custom_cmaps.cmap_bed1.N)
    
    # Make sure the color map has the correct range
    #norm = colors.Normalize(vmin=vmin, vmax=vmax)
    # Plot the data      
    self.cs = tripcolor(x,y,self.tri_cells,self.v,norm=norm,shading='gouraud',cmap = custom_cmaps.cmap_bed1)
    
    position= self.fig.add_axes([.8,.695,0.018,0.13])
    

    cbar = self.fig.colorbar(self.cs,position)
    
    plt.tick_params(labelsize = 13)
    # Define the tick marks and tick labels
    ticks = [-5000,-4000,-3000,-2000,-1000,0,1000,2000,3000,3600]
    tick_labels = map(str,ticks)
    #tick_labels[0] = r'$\leq$ -1000'
    cbar.set_ticks(ticks)
    cbar.set_ticklabels(tick_labels)
    
    # Color bar label
    cbar.set_label('Elevation (m from sea level)')
      
  # Draw parallels and meridians
  def plot_meridians(self) :
    meridians = [0,30,60,90,120,150,-30,-60,-90,-120,-150,180]
    parallels = [-70,-80]
    self.m.drawmeridians(meridians, color='black', linewidth=.5, latmax = 90, labels = [True,True,True,True])
    self.m.drawparallels(parallels, color='black', linewidth=.5, labels = [True, True, True, True])
  
  # Plots a countour indicating where ice shelves are
  def plot_shelves(self) :
    print "Plotting shelves..."
    shelf1 = loadtxt('data/ronne_filchner_basemap.out')
    shelf2 = loadtxt('data/ross_basemap.out')
    
    plt.plot(shelf1[:,0], shelf1[:,1], 'k--', linewidth = 0.25, dashes = (1,1))
    plt.plot(shelf2[:,0], shelf2[:,1], 'k--', linewidth = 0.25, dashes = (1,1))

  # Plots the grounding line contour
  def plot_grounding_line(self) :
    print "Plotting grounding line..."
    cont = loadtxt('data/grounding_basemap.out')
    
    color = '#0040C9'
    plt.plot(cont[:,0], cont[:,1], color = 'w', linewidth = 1)
    plt.plot(cont[:,0], cont[:,1], 'b.', linewidth = 0.5)
    
  # Plots the full continent contour generated from the bedmap2 data
  def plot_continent(self) :
    print "Plotting continent..."
    cont = loadtxt('data/continent_basemap.out')
    
    plt.plot(cont[:,0], cont[:,1], color = 'w', linewidth = 1.0)
    plt.plot(cont[:,0], cont[:,1], color = 'k', linewidth = 0.5)

# Load the bedrock data
mesh = Mesh('meshes/bed_mesh_5km.xml')
Q = FunctionSpace(mesh,'CG',1)
bed = Function(Q)
File('data/bed_5km.xml') >> bed

ap = AntarcticaPlot(bed)
ap.plot()