#!/usr/bin/python
import matplotlib.pyplot as plt
from pylab import *

# http://nbviewer.ipython.org/github/jrjohansson/scientific-python-lectures/blob/master/Lecture-4-Matplotlib.ipynb

class kOmegaLine():
    def __init__(self):
      self.k=[]
      self.omega=[]
      self.nut=[]
      self.y=[]
class ULine(object):
    def __init__(self):
      self.uX=[]
      self.uY=[]
      self.uZ=[]
      self.y=[]


def readULineDataTurb(filePath):
    fil = open(filePath,'r')
    retval = kOmegaLine()
    for line in fil:
      row = [x.strip(' \t\n\r') for x in line.split(' \t')]
      retval.y.append(row[0])
      retval.k.append(row[1])
      retval.nut.append(row[2])
      retval.omega.append(row[3])
    return retval
  
def readULineData(filePath):
    fil = open(filePath,'r')
    retval = ULine()
    for line in fil:
      row = [x.strip(' \t\n\r') for x in line.split(' \t')]
      retval.y.append(float(row[0]))
      retval.uX.append(float(row[1]))
      retval.uY.append(float(row[2]))
      retval.uZ.append(float(row[3]))
    return retval

def main(path, id):
  filePathTemplate='{0}/postProcessing/sets/{1}/lineL1_U.xy'.format(path, id)  
  modelResult = readULineData(filePathTemplate)
  
  filePathTemplate='{0}/postProcessing/sets/{1}/lineL1_k_nut_omega.xy'.format(path, id)
  modelResultTurb = readULineDataTurb(filePathTemplate)
  
  
  fig = subplot(4,1,1)
  plot(modelResult.uX,modelResult.y,'k')
  fig.set_title('U')
  
  fig = subplot(4,1,2)
  plot(modelResultTurb.k,modelResultTurb.y,'k')
  fig.set_title('k')
  
  fig = subplot(4,1,3)
  plot(modelResultTurb.nut,modelResultTurb.y,'k')
  fig.set_title('nut')
  
  fig = subplot(4,1,4)
  plot(modelResultTurb.omega,modelResultTurb.y,'k')
  fig.set_title('omega/epsilon')
  show()
    
     
  
if __name__ == "__main__":
  if (len(sys.argv) == 1) or (len(sys.argv) == 2):
    print "arg1: openfoam folder, arg2 is the time step"
  else:
    main(sys.argv[1], sys.argv[2])
