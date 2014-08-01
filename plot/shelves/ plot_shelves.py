"""
Create contours for the Antarctic ice shelves so we can plot them. 
"""

from pylab import *
from numpy import *

# Load the shelf data
shelf1 = loadtxt('shelf1_cont.out')
shelf2 = loadtxt('shelf2_cont.out')

plot(shelf1[:,0], shelf1[:,1])
plot(shelf2[:,0], shelf2[:,1])
show()