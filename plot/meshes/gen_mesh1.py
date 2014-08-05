from varglas.utilities import DataInput, MeshGenerator, MeshRefiner
from varglas.data.data_factory import DataFactory
from pylab import *


#===============================================================================
# data preparation :
thklim = 0.0

# create meshgrid for contour :
bedmap2 = DataFactory.get_bedmap2()

# process the data :
db2 = DataInput(bedmap2, gen_space=False)
#db2.set_data_val("H", 32767, thklim)
#db2.set_data_val('S', 32767, 0.0)
#
#db2.data['B'] = db2.data['S'] - db2.data['H']
#
#gradS = gradient(db2.data['S'])
#gS_n = sqrt(gradS[0]**2 + gradS[1]**2) + 1
#
#db2.data['ref'] = db2.data['H'] / gS_n


#db2.data['mask'][db2.data['mask'] == 1] = 100
#db2.data['mask'][db2.data['mask'] == 127] = 0
#db2.data['mask'][db2.data['mask'] == 1] = 0

# plot to check :
#db2.data['mask'][db2.data['mask'] == 1] = 0
#imshow(db2.data['mask'][::-1,:])
#colorbar()
#tight_layout()
#show()

imshow(db2.data['B'][::-1])
colorbar()
#show()
print db2.data['B'].max()

# generate the contour :
m = MeshGenerator(db2, 'mesh', '')

# Manually create a circular contour
angles = linspace(0, 1, 1000)*2*pi
xs = 2999000*cos(angles)
ys = 2999000*sin(angles)
contour = array(zip(xs, ys))

m.set_contour(contour)

m.write_gmsh_contour(1000, boundary_extend=False)
m.add_edge_attractor(1)
#field, ifield, lcMin, lcMax, distMin, distMax
m.add_threshold(2, 1, 5000, 5000, 1, 100000)
m.finish(4)
m.close_file()

