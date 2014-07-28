# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 16:12:36 2014

@author: jake
"""

""" Script that takes in lat,lon gps coordinates and returns the x,y coordinates."""
from pylab import *
from mpl_toolkits.basemap import Basemap
from varglas.data.data_factory import DataFactory
from varglas.utilities import DataInput, MeshGenerator
from numpy import *


# Get the Antarctica data sets
bedmap2 = DataFactory.get_bedmap2(thklim = 200)

db2 = DataInput(bedmap2)
db2.set_data_val('mask',1,127)

mg = MeshGenerator(db2, 'mesh', '')
mg.create_contour('mask', 0, skip_pts=25)
mg.eliminate_intersections(dist=40)
cxs = mg.longest_cont[:,0]
cys = mg.longest_cont[:,1]


#print(m.longest_cont)
#m.plot_contour()


# Create the basemap plot
proj   = 'stere'
lat_0  = '-90'
lat_ts = '-71'
lon_0  = '0'
    
width = 3333500*2
height = 3333500*2

"""m = Basemap(width=width, height=height, resolution='h',
projection="stere", lat_ts=lat_ts, lon_0=lon_0, lat_0=lat_0)"""

# Load the glacier data
glacier_data = loadtxt('glacier_data.out', delimiter = '|', dtype = 'str')
lons = array(glacier_data[:,1], dtype = 'f')
lats = array(glacier_data[:,2], dtype = 'f')

# Convert lons and lats to x, y coordinates
x, y = db2.p(lons,lats)

plot(cxs,cys,'bo-',ms = 1)
plot(x,y,'ro',ms = 2)
show()

#m.drawcoastlines(linewidth=0.25, color = 'black') 
#m.scatter(x, y, 3, marker='o', color='r')
#show()
