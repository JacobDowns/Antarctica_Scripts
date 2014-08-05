# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 16:44:39 2014

@author: jake
"""
from matplotlib.colors import LinearSegmentedColormap
import pickle

# Create a wiki color map
d_wiki = pickle.load( open( "color_maps/wiki.p", "rb" ) )
cmap_wiki = LinearSegmentedColormap('wiki', d_wiki)

# Create an Antarctica bed color map
d_bed = pickle.load( open( "color_maps/antarctica.p", "rb" ) )
cmap_bed = LinearSegmentedColormap('bed', d_bed)

# Alternate version
d_bed1 = pickle.load( open( "color_maps/antarctica1.p", "rb" ) )
cmap_bed1 = LinearSegmentedColormap('bed1', d_bed1)
