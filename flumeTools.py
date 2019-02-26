#!/usr/bin/python
'''
This is a module specifically for analyzing the results of the flume experiments
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
from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
    sys.path.append("/home/pgrover/working/working/Code/PatFoamLib/code")
else:
    sys.path.append(r"C:\working\Code\PatFoamLib\code")
import os
import numpy as np
import scipy.io
from pylab import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
#import volVectorFieldLib
import SampleLineLib
import experimentalDataLib
import adv_tools


def clean_velocities(dunedb_path_in,dune_db_out, m=2.5):
    Dunedb = scipy.io.loadmat(dunedb_path_in, struct_as_record=False, squeeze_me=True)

    for dune_id in range(2):
        dune1 = Dunedb['Dune'][dune_id]
        for profile_id in range(dune1.NumProfiles):
            for test_id in range(2):
                profiles = dune1.Profile[profile_id].Test[test_id]
                profile_station = dune1.Profile[profile_id].Station
                profile_bed = dune1.Profile[profile_id].BedElevation
                u = []
                z = []
                for cell_id in range(profiles.NumCells):
                    cell = profiles.Cell[cell_id]
                    Uxf2, Uyf2, Uzf2 = adv_tools.clean_velocities(profiles.Cell[cell_id].Uxf, profiles.Cell[cell_id].Uyf, profiles.Cell[cell_id].Uzf, m)
                    Dunedb['Dune'][dune_id].Profile[profile_id].Test[test_id].Cell[cell_id].Uxf2=Uxf2
                    Dunedb['Dune'][dune_id].Profile[profile_id].Test[test_id].Cell[cell_id].Uyf2=Uyf2
                    Dunedb['Dune'][dune_id].Profile[profile_id].Test[test_id].Cell[cell_id].Uzf2=Uzf2

                    print('Finished dune: %s, profile_id: %s, test_id: %s, cell: %s ' % (dune_id, profile_id, test_id, cell_id))

    scipy.io.savemat(dune_db_out, Dunedb, False)







def get_velocities(Dunedb, dune_id, profile_id,test_id, remove_bed_elevation=True):
    ''' Extracts the velocities and calculates the mean velocity'''

    dune = Dunedb['Dune'][dune_id]
    profile = dune.Profile[profile_id].Test[test_id]
    profile_bed = dune.Profile[profile_id].BedElevation

    ulab = []
    zlab = []
    for j in range(profile.NumCells):
        cell = profile.Cell[j]
        if cell.Z > profile_bed and cell.CellNumber > 2:
            ulab.append( np.median(cell.Uxf) )
            if remove_bed_elevation == True:
                zlab.append(cell.Z - profile_bed)
            else:
                zlab.append(cell.Z)
    return ulab, zlab

def get_tau_xz(Dunedb, dune_id, profile_id,test_id, scale=1, m=2.5, remove_bed_elevation=True, density=1000.):
    dune = Dunedb['Dune'][dune_id]
    profile = dune.Profile[profile_id].Test[test_id]
    profile_bed = dune.Profile[profile_id].BedElevation

    taulab = []
    zlab = []
    for j in range(profile.NumCells):
        cell = profile.Cell[j]
        if cell.Z > profile_bed and cell.CellNumber > 2 and cell.CellNumber < 11:
            if remove_bed_elevation == True:
                zlab.append(cell.Z - profile_bed)
            else:
                zlab.append(cell.Z)

            #Uxf, Uyf, Uzf = adv_tools.clean_velocities(cell.Uxf, cell.Uyf, cell.Uzf,1.5)
            
            Uxf = cell.Uxf2[200:]
            Uyf = cell.Uyf2[200:]
            Uzf = cell.Uzf2[200:]

            ''' Now calculate the turbulent kinetic energy'''
            Ux = np.mean(Uxf)
            uxprime = Uxf - Ux           

            #Uy = np.mean(Uyf)
            #uyprime = Uyf - Uy

            Uz = np.mean(Uzf)
            uzprime = Uzf - Uz
            
            tau = np.mean(uxprime * uzprime) * density * -1.0

            taulab.append( tau )

    return taulab, zlab

def get_k(Dunedb, dune_id, profile_id,test_id, scale=1, m=2.5, remove_bed_elevation=True):

    dune = Dunedb['Dune'][dune_id]
    profile = dune.Profile[profile_id].Test[test_id]
    profile_bed = dune.Profile[profile_id].BedElevation

    klab = []
    zlab = []
    for j in range(profile.NumCells):
        cell = profile.Cell[j]
        if cell.Z > profile_bed and cell.CellNumber > 2 and cell.CellNumber < 11:
            if remove_bed_elevation == True:
                zlab.append(cell.Z - profile_bed)
            else:
                zlab.append(cell.Z)

            #Uxf, Uyf, Uzf = adv_tools.clean_velocities(cell.Uxf, cell.Uyf, cell.Uzf,1.5)
            
            Uxf = cell.Uxf2[200:]
            Uyf = cell.Uyf2[200:]
            Uzf = cell.Uzf2[200:]

            ''' Now calculate the turbulent kinetic energy'''
            Ux = np.mean(Uxf)
            uxprime = Uxf - Ux
            

            Uy = np.mean(Uyf)
            uyprime = Uyf - Uy

            Uz = np.mean(Uzf)
            uzprime = Uzf - Uz

            uxprimebar = uxprime * uxprime
            uyprimebar = uyprime * uyprime
            uzprimebar = uzprime * uzprime

            k = 0.5*( np.mean(uxprimebar) + np.mean(uyprimebar) + np.mean(uzprimebar) )

            klab.append( k )

    return klab, zlab



def plot_velocity_profiles(modelpath, timestep, experimentaldb, test, dune):
    # Dune5_3_U.xy
    counter = 1
    col = 1
    for profile in xrange(1,13,1):
        filePathTemplate='{0}/postProcessing/sets/{1}/Dune{2}_{3}_U.xy'.format(modelpath, timestep, dune, profile)
        modelResult = SampleLineLib.read_U_line(filePathTemplate)
        modelResult.miny = min(modelResult.y)

        # Read in the experimental results
        Dunedb = scipy.io.loadmat(experimentaldb, struct_as_record=False, squeeze_me=True)

        ''' We need to correct the indexing for the dune database'''
        dune_id = dune
        if dune_id == 5:
            dune_id = 0
        elif dune_id == 6:
            dune_id=1

        ulab, zlab = get_velocities(Dunedb, dune_id,profile-1,test-1)

        fig = subplot(6,3,counter)
        y0_model = [y - min(modelResult.y) for y in modelResult.y]
        plot(modelResult.uX,y0_model,'k')
        y0 = [y - min(zlab) for y  in zlab]
        plot(ulab,y0,'ro')
        fig.set_title('Profile ' + str(profile))
        if col==1:
            col = 2
        else:
            col = 1;
        counter+=1

    show()


def calc_turbulent_kinetic_enery(Ux,Uy,Uz):
    k = 0.0
    
    if len(Ux) == len(Uy) and len(Ux) == len(Uz):
        n = len(Ux)
        
        ux_mean = np.mean(Ux)
        uy_mean = np.mean(Uy)
        uz_mean = np.mean(Uz)
        
        sum_ux = 0.0
        sum_uy = 0.0
        sum_uz = 0.0
        
        for i in range(n):
            sum_ux += (Ux[i] - ux_mean)**2
            sum_uy += (Uy[i] - uy_mean)**2
            sum_uz += (Uz[i] - uz_mean)**2
            
        uxp = sum_ux / n
        uyp = sum_uy / n
        uzp = sum_uz / n
        
        k = 0.5 * (uxp + uyp + uzp)
        
    else:
        raise ValueException('The dimensions of the two arrays do not match')
    
    return k

def get_quadrants(Ux, Uy):
    
    uxprime = []
    uyprime = []
    if len(Ux) == len(Uy):
        n = len(Ux)
        
        ux_mean = np.mean(Ux)
        uy_mean = np.mean(Uy)
        
        for i in range(n):
            uxprime.append(Ux[i] - ux_mean)
            uyprime.append(Uy[i] - uy_mean)

    return np.array(uxprime),np.array(uyprime)


def calc_covariance(Ux, Uy):
    '''
    Eq. 2.24 from
    http://digitool.library.colostate.edu/webclient/DeliveryManager?pid=111587
    '''
    cov_xy = None
    if len(Ux) == len(Uy):
        n = len(Ux)
        sum_uv = 0.0
        sum_u = 0.0
        sum_v = 0.0
        for i in range(n):
            sum_uv += Ux[i] * Uy[i]
            sum_u += Ux[i]
            sum_v += Uy[i]
        cov_xy = ( sum_uv/(n-1.0) ) - ( (sum_u*sum_v)/(n*(n-1)) )
    else:
        raise ValueException('The dimensions of the two arrays do not match')

    return cov_xy




def plot_turb_profiles(modelpath, timestep, experimentaldb, test, dune):
    # Dune5_3_U.xy
    counter = 1
    col = 1
    for profile in xrange(1,13,1):
        filePathTemplate='{0}/postProcessing/sets/{1}/Dune{2}_{3}_k_nut_omega.xy'.format(modelpath, timestep, dune, profile)
        modelResult = SampleLineLib.read_turb_line(filePathTemplate)
        modelResult.miny = min(modelResult.y)

        ''' We need to correct the indexing for the dune database'''
        dune_id = dune
        if dune_id == 5:
            dune_id = 0
        elif dune_id == 6:
            dune_id=1
        Dunedb = scipy.io.loadmat(experimentaldb, struct_as_record=False, squeeze_me=True)
        klab, zlab = get_k(Dunedb, dune_id,profile-1,test-1)

        fig = subplot(6,3,counter)
        y0_model = [y - min(modelResult.y) for y in modelResult.y]
        plot(modelResult.k,y0_model,'k')
        y0 = [y - min(zlab) for y  in zlab]
        plot(klab,y0,'ro')
        fig.set_title('Profile ' + str(profile))
        if col==1:
            col = 2
        else:
            col = 1;
        counter+=1

    show()
    
def main():
    path_in = '/home/pgrover/working/working/Paper_2_Flume_Modelling/ADV Measurements/database/Dunes_v004.mat'
    path_out = '/home/pgrover/working/working/Paper_2_Flume_Modelling/ADV Measurements/database/Dunes_v005.mat'

    clean_velocities(path_in,path_out, 2.5)

if __name__ == '__main__':
    main()

