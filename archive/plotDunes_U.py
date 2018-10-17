#!/usr/bin/python
import matplotlib.pyplot as plt
from pylab import *

class ULine(object):
    def __init__(self):
      self.uX=[]
      self.uY=[]
      self.uZ=[]
      self.y=[]
      self.miny=0
      

def readULineData(filePath):
    fil = open(filePath,'r')
    retval = ULine()
    for line in fil:
      row = [x.strip(' \t\n\r') for x in line.split(' \t')]
      retval.y.append(float(row[0]))
      retval.uX.append(float(row[1]))
      retval.uY.append(float(row[2]))
      retval.uZ.append(float(row[3]))
    retval.miny = min(retval.y)
    return retval
  
def readUADVData(filePath):
    fil = open(filePath,'r')
    retval = ULine()
    for line in fil:
      row = [x.strip(' \t\n\r') for x in line.split(',')]
      retval.y.append(float(row[1]))
      retval.uX.append(float(row[2]))
      retval.uZ.append(float(row[3]))
    return retval
  
def main(path, id):
  # Dune5_3_U.xy
  
  counter = 1
  col = 1
  for profile in xrange(1,13,1):
    filePathTemplate='{0}/postProcessing/sets/{1}/Dune{2}_{3}_U.xy'.format(path, id, 6, profile)  
    modelResult = readULineData(filePathTemplate)
    
    # Dune_2_Test_1_Profile_1.csv
    #E:\Paper_4\FlumeExperiment\csv\Dune2\Test1
    filePathTemplate='csv/Dune2/Test1/Dune_2_Test_1_Profile_{0}.csv'.format(profile)  
    labResult = readUADVData(filePathTemplate)
 
    fig = subplot(6,2,counter)
    y0_model = [y - modelResult.miny for y in modelResult.y]
    plot(modelResult.uX,y0_model,'k')
    y0 = [y - labResult.miny for y  in labResult.y]
    plot(labResult.uX,y0,'ro')
    fig.set_title('Profile ' + str(profile))
    if col==1:
	col = 2;
    else:
        col = 1;
    counter+=1

  show()
  
if __name__ == "__main__":
  if (len(sys.argv) == 1) or (len(sys.argv) == 2):
    print "arg1: openfoam folder, arg2 is the time step"
  else:
    main(sys.argv[1], sys.argv[2])
