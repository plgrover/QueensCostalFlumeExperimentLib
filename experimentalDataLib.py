
#!/usr/bin/python
'''
This is a module specifically for reading experimental data collected in the
flume using the Vectrino II ADV
'''
__author__ = "Patrick Grover"
__copyright__ = ""
__credits__ = ["Patrick Grover"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Patrick Grover"
__email__ = ""
__status__ = "Development"

import sys
sys.path.append("/home/geeko/working/Code/PatFoamLib/code")
import SampleLineLib

class adv_line(object):
    def __init__(self):
      self.uX=[]
      self.uY=[]
      self.uZ=[]
      self.y=[]
      self.k = []
      self.nut = []
      self.omega = []
      self.miny = 0


def read_u_adv_data(filePath):
    fil = open(filePath,'r')
    retval = adv_line()
    for line in fil:
      row = [x.strip(' \t\n\r') for x in line.split(',')]
      retval.y.append(float(row[1]))
      retval.uX.append(float(row[2]))
      retval.uZ.append(float(row[3]))
      retval.k.append(float(row[9]))
    return retval