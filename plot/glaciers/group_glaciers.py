# -*- coding: utf-8 -*-
""" 
Somehow figure out how to group the glaciers...
"""

from pylab import *
from numpy import *
from pyproj import Proj

proj   = 'stere'
lat_0  = '-90'
lat_ts = '-71'
lon_0  = '0'
    
# Setup a projection
proj =   " +proj=" + proj \
           + " +lat_0="  + lat_0 \
           + " +lat_ts=" + lat_ts \
           + " +lon_0="  + lon_0 \
           + " +k=1 +x_0=0 +y_0=0 +no_defs +a=6378137 +rf=298.257223563" \
           + " +towgs84=0.000,0.000,0.000 +to_meter=1"
           
p = Proj(proj)

# Load a continent contour
ground = loadtxt('../data/grounding_cont.out')
continent = loadtxt('../data/continent_cont.out')

# Convert from (lon,lat) to bedmap2 coordinates
ground_xs, ground_ys = p(ground[:,0], ground[:,1])
continent_xs, continent_ys = p(continent[:,0], continent[:,1])

# Load the glacier data
glacier_data = loadtxt('outlet_glaciers.out', delimiter = '|', dtype = 'str')
glacier_names = array(glacier_data[:,0], dtype = 'str')
glacier_lons = array(glacier_data[:,1], dtype = 'f')
glacier_lats = array(glacier_data[:,2], dtype = 'f')


# Convert to basemap coordinates
xs, ys = p(glacier_lons, glacier_lats)

d = {}
# Create a dictionary from the glacier data
for i in range(len(glacier_names)) :
  lon = glacier_lons[i]
  lat = glacier_lats[i]
  name = glacier_names[i]
  
  d[name] = array([name,lon,lat])

# Plot grounding line
plot(ground_xs, ground_ys, 'k')
# Plot ice extent
plot(continent_xs, continent_ys, 'k')
# Plot glaciers
plot(xs, ys ,'ro', ms = 5)

# Plot the glacier names
for i in range(len(xs)) :
  x = xs[i]
  y = ys[i]
  name = glacier_names[i]
  
  text(x, y, unicode(name), fontsize=12)
  
show()

group1 = []
group1.append(d['Arena Glacier'])
group1.append(d['Kenney Glacier'])
group1.append(d['Depot Glacier'])
group1.append(d['Mondor Glacier'])
group1.append(d['Hektoria Glacier'])
group1.append(d['Punchbowl Glacier'])
group1.append(d['Crane Glacier'])
group1.append(d['Melville Glacier'])
group1.append(d['Rachel Glacier'])
group1.append(d['Starbuck Glacier'])
group1.append(d['Stubb Glacier'])
group1.append(d['Sleipnir Glacier'])
group1.append(d['Stubb Glacier'])
group1.append(d['Fricker Glacier'])
group1.append(d['Chamberlin Glacier'])
group1.append(d['Robillard Glacier'])
group1.append(d['Maitland Glacier'])
group1.append(d['Earnshaw Glacier'])
group1.append(d['Cronus Glacier'])
group1.append(d['Lurabee Glacier'])
group1.append(d['Bingham Glacier'])
group1.append(d['Anthony Glacier'])
group1.append(d['Cordini Glacier'])
group1.append(d['Clifford Glacier'])
group1.append(d['Yates Glacier'])
group1.append(d['Dana Glacier'])
group1.append(d['Gain Glacier'])
group1.append(d['Gruening Glacier'])
group1.append(d['Spiess Glacier'])
group1.append(d['Maury Glacier'])
group1.append(d['Heezen Glacier'])
group1.append(d['Wells Glacier'])
group1.append(d['Ketchum Glacier'])

savetxt('groups/group1.out', group1, delimiter = '|',  fmt="%s")

group2 = []
group2.append(d['Russell East Glacier'])
group2.append(d['Renard Glacier'])
group2.append(d['Bayly Glacier'])
group2.append(d['Leonardo Glacier'])
group2.append(d['Green Glacier'])
group2.append(d['Archer Glacier'])
group2.append(d['Niépce Glacier'])
group2.append(d['Daguerre Glacier'])
group2.append(d['Hotine Glacier'])
group2.append(d['Leay Glacier'])
group2.append(d['Wiggins Glacier'])
group2.append(d['Bussey Glacier'])
group2.append(d['Lind Glacier'])
group2.append(d['Luke Glacier'])
group2.append(d['Bradford Glacier'])
group2.append(d['Bilgeri Glacier'])
group2.append(d['Hugi Glacier'])
group2.append(d['Antevs Glacier'])
group2.append(d['Lliboutry Glacier'])
group2.append(d['Bader Glacier'])
group2.append(d['Somigliana Glacier'])
group2.append(d['Saussure Glacier'])
group2.append(d['Swithinbank Glacier'])
group2.append(d['Todd Glacier'])
group2.append(d['Prospect Glacier'])
group2.append(d['Zephyr Glacier'])
group2.append(d['Zonda Glacier'])
group2.append(d['Hill Glacier'])
group2.append(d['Nikitin Glacier'])
group2.append(d['Gopher Glacier'])
group2.append(d['Exum Glacier'])
group2.append(d['Haskell Glacier'])
group2.append(d['Rosanova Glacier'])
group2.append(d['Rignot Glacier'])
group2.append(d['Pope Glacier'])
group2.append(d['Smith Glacier'])
group2.append(d['Yoder Glacier'])
group2.append(d['Horrall Glacier'])
group2.append(d['Dorchuck Glacier'])

savetxt('groups/group2.out', group2, delimiter = '|',  fmt="%s")

group3 = []
group3.append(d['Frostman Glacier'])
group3.append(d['Lord Glacier'])
group3.append(d['Clarke Glacier'])
group3.append(d['Shuman Glacier'])
group3.append(d['Anandakrishnan Glacier'])
group3.append(d['Reynolds Glacier'])
group3.append(d['Hammond Glacier'])
group3.append(d['Jacobel Glacier'])
group3.append(d['Dalton Glacier'])
group3.append(d['Hamilton Glacier'])

savetxt('groups/group3.out', group3, delimiter = '|',  fmt="%s")

group4 = []
group4.append(d['Roe Glacier'])
group4.append(d['Krout Glacier'])
group4.append(d['Holzrichter Glacier'])
group4.append(d['McCuistion Glacier'])
group4.append(d['Dick Glacier'])
group4.append(d['Gerasimou Glacier'])
group4.append(d['Forman Glacier'])
group4.append(d['Perez Glacier'])
group4.append(d['Beardmore Glacier'])
group4.append(d['Socks Glacier'])
group4.append(d['Robb Glacier'])
group4.append(d['Perez Glacier'])
group4.append(d['Kent Glacier'])
group4.append(d['Rowland Glacier'])
group4.append(d['Tranter Glacier'])
group4.append(d['Dickey Glacier'])
group4.append(d['Starshot Glacier'])
group4.append(d['Mason Glacier'])
group4.append(d['Koettlitz Glacier'])
group4.append(d['Cassini Glacier'])
group4.append(d['Harbour Glacier'])
group4.append(d['Perez Glacier'])
group4.append(d['Oates Piedmont Glacier'])
group4.append(d['Perez Glacier'])
group4.append(d['Harbord Glacier'])
group4.append(d['Ridgeway Glacier'])
group4.append(d['Mariner Glacier'])
group4.append(d['Borchgrevink Glacier'])
group4.append(d['Burnette Glacier'])
group4.append(d['Nameless Glacier'])
group4.append(d['Warning Glacier'])
group4.append(d['Fendley Glacier'])
group4.append(d['Simpson Glacier'])
group4.append(d['Dennistoun Glacier'])
group4.append(d['Crawford Glacier'])
group4.append(d['Barber Glacier'])
group4.append(d['Arruiz Glacier'])
group4.append(d['Carryer Glacier'])
group4.append(d['Sledgers Glacier'])
group4.append(d['Orr Glacier'])
group4.append(d['Serrat Glacier'])
group4.append(d['Manna Glacier'])
group4.append(d['Walsh Glacier'])
group4.append(d['McLeod Glacier'])

savetxt('groups/group4.out', group4, delimiter = '|',  fmt="%s")
