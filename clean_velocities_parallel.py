#!/usr/bin/python
'''
This is a module specifically cleaning the ADV values using a parallelized code
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
import os
import numpy as np
import scipy.io
from pylab import *
import adv_tools
import tempfile
import shutil

#from multiprocessing import Process, Manager, Pool



#import mmap

from joblib import Parallel, delayed
from joblib import load, dump

def clean_velocities(cell):
    print 'Working on measurement id: %s cell, %s' % (cell.MeasurementId, cell.CellNumber)



def clean_velocities_parallel(dunedb_path_in,dune_db_out, m=2.5):
    Dunedb = scipy.io.loadmat(dunedb_path_in, struct_as_record=False, squeeze_me=True)

   #http://stackoverflow.com/questions/6832554/python-multiprocessing-how-do-i-share-a-dict-among-multiple-processes

    folder = tempfile.mkdtemp()
    temp_file_name = os.path.join(folder, 'samples')




    dunes = Dunedb['Dune']

    for dune_id in range(2):
        dune1 = Dunedb['Dune'][dune_id]
        for profile_id in range(dune1.NumProfiles):
            for test_id in range(2):

                fp = np.memmap(temp_file_name, dtype='float32', mode='w+', shape=(2,dune1.Profile[profile_id].Test[test_id].NimCells))


                profiles = dune1.Profile[profile_id].Test[test_id]

                print 'Profile: %s, Test: %s' % (profile_id,test_id)

                manager = Manager()
                Cells = manager.dict()
                for cell in profiles.Cell:
                    identifier = '%s-%s' % (cell.MeasurementId, cell.CellNumber)
                    print identifier
                    Cells[identifier] = cell


                pool = Pool()
                pool.map(clean_velocities,Cells)
                pool.close()
                pool.join()

    #scipy.io.savemat(dune_db_out, Dunedb, False)

if __name__ == '__main__':
    path_in = '/home/geeko/working/Paper_2_Flume_Modelling/ADV Measurements/database/Dunes_v004.mat'
    path_out = '/home/geeko/working/Paper_2_Flume_Modelling/ADV Measurements/database/Dunes_v005.mat'

    #clean_velocities_parallel(path_in,path_out)

    print 'Done....'




