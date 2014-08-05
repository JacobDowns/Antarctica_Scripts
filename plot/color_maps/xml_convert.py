from xml.dom import minidom
import numpy as np
import pickle

""" Script I found and modified for converting XML color maps in paraview
to a Python dictionary so they can be used with Matplotlib. I cannot 
seem to locate where I got the original script now..."""

# Takes in an xml color map and converts it to a Python dictionary for
# matplotlib.
# Set log_scale to true to log transform the color map
def parseXmlMap(fileName,log_scale = False) :
  xmlDoc = minidom.parse(fileName)
  pointList = xmlDoc.getElementsByTagName('Point')

  # List of red values at each point
  reds = []
  # List of green values at each point
  greens = []
  # List of blue values at each point
  blues = []
  # List of x values
  xVals = []

  for p in pointList :
    x = float(p.attributes['x'].value)
    r = float(p.attributes['r'].value)
    g = float(p.attributes['g'].value)
    b = float(p.attributes['b'].value)
    xVals.append(x)
    reds.append(r)
    greens.append(g)
    blues.append(b)
  
  # Normalize the array of x values so that every element is between 0 and 1
  # Get the xVals as a numpy array
  xValsNP = np.array(xVals)
  
  if log_scale :
    xValsNP += 1
    # Log transform the x values of the color map
    xValsNP = np.log(xValsNP) / np.log(xValsNP[-1])
    
  # 0-1 normalize the values
  xValsNP = xValsNP / xValsNP.max()

  def getSubTuple(i,xVals,colors) :
    return (xVals[i],colors[i],colors[i])

  # Get the number of points
  l = len(xVals)
  # Make the red, green, and blue tuples for the color dictionary
  
  # Check if the first x value is 0 (a requirement for matplotlib)
  start = 0
  if(xValsNP[0] != 0) :
    redTuple = ((0,reds[0],reds[0]),)
    greenTuple = ((0,greens[0],greens[0]),)
    blueTuple = ((0,blues[0],blues[0]),) 
    start = 0
  else :
    redTuple = (getSubTuple(0,xValsNP,reds),)
    greenTuple = (getSubTuple(0,xValsNP,greens),)
    blueTuple = (getSubTuple(0,xValsNP,blues),)
    start = 1
  
  for i in range(start,l) :
    redTuple = redTuple + (getSubTuple(i,xValsNP,reds),)
    greenTuple = greenTuple + (getSubTuple(i,xValsNP,greens),)
    blueTuple = blueTuple + (getSubTuple(i,xValsNP,blues),)

  # Now use the tuples to make the full dictionary
  colorDict = {'red' : redTuple,'green' : greenTuple,'blue' : blueTuple}
  return colorDict

cm = parseXmlMap("antarctica_bed.xml")
print cm
# Save the color map dictionary
pickle.dump( cm, open( "antarctica.p", "wb" ) )
    

