# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 16:28:28 2014

@author: jake
"""

#from scipy.io import read_array
#from scipy import zeros, linspace, shape, Float, concatenate
from numpy import *
import pickle

# Credit for this function goes to:
# http://matplotlib.1069221.n5.nabble.com/function-to-create-a-colormap-from-cpt-palette-td2165.html
def cpt2seg(file_name, sym=False, discrete=False):
    """Reads a .cpt palette and returns a segmented colormap.

    sym : If True, the returned colormap contains the palette and a mirrored copy.
    For example, a blue-red-green palette would return a blue-red-green-green-red-blue colormap.

    discrete : If true, the returned colormap has a fixed number of uniform colors.
    That is, colors are not interpolated to form a continuous range.

    Example :
    >>> _palette_data = cpt2seg('palette.cpt')
    >>> palette = matplotlib.colors.LinearSegmentedColormap('palette', _palette_data, 100)
    >>> imshow(X, cmap=palette)
    """
   
   
    dic = {}
    f = open(file_name, 'r')
    rgb = loadtxt(f)
    print rgb 
    
    rgb = rgb/255.
    s = shape(rgb)
    colors = ['red', 'green', 'blue']
    for c in colors:
        i = colors.index(c)
        x = rgb[:, i+1]

        if discrete:
            if sym:
                dic[c] = zeros((2*s[0]+1, 3), dtype='f')
                dic[c][:,0] = linspace(0,1,2*s[0]+1)
                vec = concatenate((x ,x[::-1]))
            else:
                dic[c] = zeros((s[0]+1, 3), dtype='f')
                dic[c][:,0] = linspace(0,1,s[0]+1)
                vec = x
            dic[c][1:, 1] = vec
            dic[c][:-1,2] = vec
               
        else:
            if sym:
                dic[c] = zeros((2*s[0], 3), dtype='f')
                dic[c][:,0] = linspace(0,1,2*s[0])
                vec = concatenate((x ,x[::-1]))
            else:
                dic[c] = zeros((s[0], 3), dtype='f')
                dic[c][:,0] = linspace(0,1,s[0])
                vec = x
            dic[c][:, 1] = vec
            dic[c][:, 2] = vec
   
    return dic

cm = cpt2seg('wiki.cpt', discrete = True)
# Save the color map dictionary
pickle.dump( cm, open( "wiki.p", "wb" ) )

