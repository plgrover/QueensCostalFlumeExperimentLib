
#!/usr/bin/python
'''
This is a module specific for working with the ADV code.
'''
__author__ = "Patrick Grover"
__copyright__ = ""
__credits__ = ["Patrick Grover"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Patrick Grover"
__email__ = ""
__status__ = "Development"

import numpy as np

def clean_velocities(Ux, Uy, Uz, m):
    signal = np.matrix([Ux, Uy, Uz])
    removed_value = True
    while removed_value:
        removed_value = False
        mean_Ux = np.mean(signal[0,:])
        stdev_Ux = np.std(signal[0,:])

        mean_Uy = np.mean(signal[1,:])
        stdev_Uy = np.std(signal[1,:])

        mean_Uz = np.mean(signal[2,:])
        stdev_Uz = np.std(signal[2,:])

        #print 'Expected Ux mean: %s, got: %s, std: %s' % (np.mean(Ux),mean_Ux,stdev_Ux)
        #print 'Expected Uy mean: %s, got: %s, std: %s' % (np.mean(Uy),mean_Uy,stdev_Uy)
        #print 'Expected Uz mean: %s, got: %s, std: %s' % (np.mean(Uz),mean_Uz,stdev_Uz)

        for col in range(signal.shape[1]):
            ux = signal[0,col]
            uy = signal[1,col]
            uz = signal[2,col]

            if abs(ux-mean_Ux) > m * stdev_Ux:
                signal = np.delete(signal, col, 1)
                removed_value = True
                #print 'Removed id: %s for ux: %s' % (col, ux)
                break
            elif abs(uy-mean_Uy) > m * stdev_Uy:
                signal = np.delete(signal, col, 1)
                removed_value = True
                #print 'Removed id: %s for uy: %s' % (col, uy)
                break
            elif abs(uz-mean_Uz) > m * stdev_Uz:
                signal = np.delete(signal, col, 1)
                removed_value = True
                #print 'Removed id: %s for uz: %s ' % (col, uz)
                break

    return np.squeeze((np.asarray(signal[0,:]))),np.squeeze(np.asarray(signal[1,:])),np.squeeze(np.asarray(signal[2,:]))


def main():
    Ux = np.array([1.1, 1.2, 1.3, 1.4, 1.1, 1.2, 1.3, 1.4])
    Uy = np.array([1.1, 1.2, 1.3, -1100.4, 1.1, 1.2, 1.3, 1.4])
    Uz = np.array([1.1, 1.2, 1.3, 1.4, 1.1, 1.2, 1.3, 1.4])

    ux, uy, uz = clean_velocities(Ux, Uy, Uz, 2.5)

    print(ux,uy,ux)

if __name__ == "__main__":
    main()