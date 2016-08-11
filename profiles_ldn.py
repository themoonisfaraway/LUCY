# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 16:57:02 2016

@author: Chris
"""
import numpy as np

'''
building profile for london. same as transportation but is shifted up or down in the main script
out --> numpy array
'''
def getQB(hour):
    qb_ldn_weekday =  np.array([0.004166667,0.004166667,0.008333333,0.020833333,\
                                0.033333333,0.041666667,0.054166667,0.070833333,\
                                0.0625,0.058333333,0.054166667,0.05,0.05,\
                                0.054166667,0.058333333,0.0625,0.066666667,0.075,\
                                0.058333333,0.041666667,0.033333333,0.020833333,\
                                0.0125,0.004166667])    
    return qb_ldn_weekday[hour]
#    return_profile = np.zeros(bin_count)
#    
#    for x in range(hour-bin_count,hour):
#        return_profile[x-(bin_count-hour)] = qb_ldn_weekday[x]
#        
#    return qb_ldn_weekday    
     
'''
metabolic profile for London weekday (at the moment)
given as fractions of 100, which is added to 75W
so 0 ends up as 75W, 0.5 as 125W, 1 as 175W
out --> numpy array
'''
def getQM(hour):     
    qm_ldn_weekday= np.array([0,0,0,0,0,0,0,0.5,1,1,1,1,1,1,1,1,1,0.5,0,0,0,0,0,0])    
    return qm_ldn_weekday[hour]
#    return_profile = np.zeros(bin_count)    
#    for x in range(hour-bin_count,hour):
#        return_profile[x-(bin_count-hour)] = qm_ldn_weekday[x]        
#    return qm_ldn_weekday

'''
transport profile for london weekday. all adds up to 1, peaks at rush hour
out --> numpy array
'''
def getQT(hour):
    qt_ldn_weekday = np.array([0.004166667,0.004166667,0.008333333,0.020833333,\
                                0.033333333,0.041666667,0.054166667,0.070833333,\
                                0.0625,0.058333333,0.054166667,0.05,0.05,\
                                0.054166667,0.058333333,0.0625,0.066666667,0.075,\
                                0.058333333,0.041666667,0.033333333,0.020833333,\
                                0.0125,0.004166667])
    return qt_ldn_weekday[hour]
    #qt_ldn_weekend = np.array([0.020833333,0.016666667,0.016666667,0.0125,0.0125,0.016666667,0.025,0.033333333,0.041666667,0.05,0.054166667,0.058333333,0.0625,0.066666667,0.066666667,	0.066666667	,0.066666667,0.066666667,0.058333333,0.054166667,0.045833333,0.0375,0.029166667,0.020833333])
#
#    return_profile = np.zeros(bin_count)
#    
#    for x in range(hour-bin_count,hour):
#        return_profile[x-(bin_count-hour)] = qt_ldn_weekday[x]    
#    
#    return return_profile
#     
    
        