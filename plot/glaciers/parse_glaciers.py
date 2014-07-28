# -*- coding: utf-8 -*-
"""
Parse a csv file of Antarctic glaciers.
"""
import csv
from numpy import *

i = 0

glacier_data = []

with open('glaciers.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter='|', skipinitialspace=True)
  for row in reader:
    if row[2] == "Glacier" :
      name = row[0]
      
      # Convert latitude to float
      lat = float(row[3][0:-1]) / 1e4
      if row[3][-1] == 'S' :
        lat = -lat
      
      # Convert longitude to float
      lon = float(row[4][0:-1]) / 1e4
      if row[4][-1] == 'W':
        lon = -lon
      
      glacier_data.append([name,lon,lat])

# Save the parsed data
glacier_data = array(glacier_data, dtype = 'str')
savetxt('glacier_data.out', glacier_data, delimiter = '|',  fmt="%s")

      
    