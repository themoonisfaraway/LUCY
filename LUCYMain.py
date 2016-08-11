# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 10:19:28 2016

@author: xp898648
"""
import numpy as np
import profiles_ldn as ldn
import f90nml
import datetime as dt
from matplotlib import pyplot as plt

'''
the start  
'''
nmlName = 'Config'
nml = f90nml.read(nmlName +'.nml')
bin_count = nml[nmlName]['bincount']
population = nml[nmlName]['population']
area = nml[nmlName]['area']
temperature = nml[nmlName]['temperature']
vehicle_count = nml[nmlName]['vehiclecount']
date = nml[nmlName]['date']
time = nml[nmlName]['time']
avg_speed =  nml[nmlName]['avgspeed']
large_area_population = nml[nmlName]['largeareapopulation']
large_area_energy_use = nml[nmlName]['largeareaenergyuse']
emission_factors = nml[nmlName]['emissionfactors']   
fig_size = nml[nmlName]['figuresize']
area_name = nml[nmlName]['areaname']
'''
returns multiplication factor to account for increased energy use by buildings
due to heating/air conditioning
set to 0.7 at 12c
increased by 0.03% for every 1c increase
decreased by 0.05% for every 1c decrease
capped at -4c and 35c: reverts to 1
'''
def getTMF(temperature):
    if temperature == 12:
        return 0.7
    if temperature <= -4 or temperature >= 35:
        return 1
    if temperature > 12:
        return 0.7 + 0.7*(0.03*(temperature-12))
    else:
        return 0.7 - 0.7*(0.05*(12-temperature))       
    
'''
returns metabolic heat flux 
met_profile: profile for emissions per person [W] dependent on time/day of week 
'''
def qm(population_density, profile):           
    Qm = population_density*(75+(100*profile)) # 0 = 75W, 1 = 175W
    
    return Qm
        
'''
energy profile is based "loosely" on the vehicle weekend profile (more-or-less gaussian shaped)
TMF scales the whole thing based on the outside temperature 
'''        
def qb(population_density, large_area_population, national_energy_use, temperature, profile):

#    if type(temperature) == np.array:
#            Qb = np.zeros(24)
#        for t in temperature:
#        #qbTimeSeries[t] = getTMF(temperature[t])*(popDensity/nationalPopulation)*national_energy_use*energyProfile[t]
#            Qb[t] = getTMF(temperature)*(popDensity/nationalPopulation)*national_energy_use*energyProfile[t]
#    else:
#        Qb = getTMF(temperature)*(popDensity/nationalPopulation)*national_energy_use*energyProfile[t]
    Qb = getTMF(temperature)*(population_density/large_area_population)*national_energy_use*profile
    return Qb
    
'''
distance --> distance driven/hour determined from no. vehicles and average speed
vehicles --> vehicle counts for each class (i think this would work for a per-person or a national/area total)
day --> chooses the profile used. 0 is weekday, 1 is weekend. probably not ideal
'''    
def qt(population_density, large_area_population, avg_speed, vehicle_count, emission_factors, profile, national):    

    distance = avg_speed*(vehicle_count[0]+vehicle_count[1]+vehicle_count[2])#eg. 48kmh --> 48*numbervehicles [km]       
    
#    if day == 0: #weekday
#        mult_factor = 1
#    elif day == 1:#weekend
#        mult_factor = 0.8
    mult_factor=0.8
    total_vehicles_withemissions =  vehicle_count[0]*emission_factors[0] +\
                                    vehicle_count[1]*emission_factors[1] +\
                                    vehicle_count[2]*emission_factors[2]
                                        
  
    Qt = mult_factor*population_density*distance*total_vehicles_withemissions*profile
    
    '''
    if vehicle_count is given per person then no need to use fraction of a
    larger population (eg. pop. density of London/pop. of UK)
    '''
    if national == 0: #per person 
        return Qt    
    else: # as fraction of a larer population
        return Qt/large_area_population

date = dt.date(date[0],date[1],date[2])
population_density = population/area   
string_day = date.strftime("%A %d. %B %Y")
print(string_day)
plt.figure(figsize=(fig_size[0],fig_size[1]))

xTicks=np.arange(0,24,4)
xlabels = ['0:00','4:00','8:00','12:00','16:00','20:00']
plt.xlabel('time [hour]')
plt.ylabel('Q$_F$ [W m${^2}$]')
plt.gca().set_xticks(xTicks)
plt.gca().set_xticklabels(xlabels)
plt.title('Q$_F$ - ' + area_name +', ' + date.strftime("%A %d. %B %Y") )
plot_values = list()
'''
this will be done outside this script eventually
'''
for t in range(time[0]-bin_count,time[0]):        
    qm_profile = ldn.getQM(t)
    qb_profile = ldn.getQB(t)
    qt_profile = ldn.getQT(t)

    Qm = qm(population_density, qm_profile)
    Qb = qb(population_density, large_area_population, large_area_energy_use, temperature, qb_profile)
    Qt = qt(population_density, large_area_population, avg_speed, vehicle_count, emission_factors, qt_profile, 1)
    
    Qf = Qm + Qb + Qt
    plot_values.append(Qf)
    
plt.plot(range(time[0]),plot_values)
'''
make plot
''' 
plt.xlim(0,24)
plt.show()
