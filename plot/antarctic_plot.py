# -*- coding: utf-8 -*-
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
from pyproj import Proj

rc('font',**{'size'   : 22})

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
    
    # Create a projection object
    proj   = 'stere'
    lat_0  = '-90'
    lat_ts = '-71'
    lon_0  = '0'
        
    # Setup a projection object
    proj =   " +proj=" + proj \
               + " +lat_0="  + lat_0 \
               + " +lat_ts=" + lat_ts \
               + " +lon_0="  + lon_0 \
               + " +k=1 +x_0=0 +y_0=0 +no_defs +a=6378137 +rf=298.257223563" \
               + " +towgs84=0.000,0.000,0.000 +to_meter=1"
               
    self.p = Proj(proj)
    
    # Get lon,lat coordinates of the mesh vertices
    self.v_lons,self.v_lats = self.p(vxs, vys,inverse=True)
  
  # Draw the outline of Greenland and the meridians
  def plot(self) :
    print("Plotting...")
    self.fig = plt.figure(figsize=(32,36))
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
    
    # Plot glacier labels
    group1 = self.load_glaciers('data/groups/group1.out')
    self.plot_group(group1, .95e6, 5.5e6, .4e5, mo = .4e5,xo = .4e5, direction = -1)
    
    self.plot_data()

    savefig('bed1.png',dpi = 300)
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
    
    #color = '#0040C9'
    plt.plot(cont[:,0], cont[:,1], 'k', linewidth = .8)
    plt.plot(cont[:,0], cont[:,1], color = '#75BFFF', linewidth = .5)
    
  # Plots the full continent contour generated from the bedmap2 data
  def plot_continent(self) :
    print "Plotting continent..."
    cont = loadtxt('data/continent_basemap.out')
    
    plt.plot(cont[:,0], cont[:,1], color = 'w', linewidth = .95)
    plt.plot(cont[:,0], cont[:,1], 'k', linewidth = .55)
  
  # Draw a label pointing to a specific point
  # (lx, ly) : label x and y
  # (tx, ty) : target x and y
  # mo : How far to the right or left the midpoint is from the label
  # text : label text
  def add_line_label(self, lx, ly, tx, ty, text, mo = 1e6, direction = 1, font_size = 13) :
    # Find the (x,y) coordinates of the midpoint
    mx = lx + direction*mo
    my = ly
    
    # Define the line properties of the label
    props = dict(arrowstyle='-',linewidth=.5)
    
    # The annotate command doesn't draw the line all the way to the midpoint so 
    # I have to nudge it in the right direction a bit
    nudge = 6500
    
    # Draw label and a line to the midpoint
    plt.annotate(text, xy=(mx + direction*nudge,my), xytext=(lx,ly),size = font_size, 
                 arrowprops = props
            )
    
    #plt.plt([lx,tx,mx],[lx,tx,mx])
    # Draw another line from the midpoint to the glacier itself
    plt.plot([mx, tx], [my, ty], 'k-', lw = .5)
  
  # Plot a group of glacier labels 
  def plot_group(self, group, sx, sy, yo, mo = 1e6, direction = 1, xo = 0) :
    for i in range(len(group[0])) :
      name = group[0][i]
      tx = group[1][i]
      ty = group[2][i]
      
      lx = sx + i*xo
      ly = sy - i*yo
      
      self.add_line_label(lx, ly, tx, ty, name, mo = mo, direction = direction)

  def load_glaciers(self, file_name) :
    # Load some glacier data
    glacier_data = loadtxt(file_name, delimiter = '|', dtype = 'str')
    glacier_names = array(glacier_data[:,0], dtype = 'str')
    glacier_lons = array(glacier_data[:,1], dtype = 'f')
    glacier_lats = array(glacier_data[:,2], dtype = 'f')    
    
    # Convert to basemap coordinates
    glacier_xs, glacier_ys = self.m(glacier_lons, glacier_lats)
    
    return (glacier_names, glacier_xs, glacier_ys)
    
# Load the bedrock data
mesh = Mesh('meshes/bed_mesh_5km.xml')
Q = FunctionSpace(mesh,'CG',1)
bed = Function(Q)
File('data/bed_5km.xml') >> bed

ap = AntarcticaPlot(bed)
ap.plot()