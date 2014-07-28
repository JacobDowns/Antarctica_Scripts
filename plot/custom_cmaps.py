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