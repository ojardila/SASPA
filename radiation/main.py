#!/usr/bin/python2.7
import math
from LatLon import Latitude

#Initial Variables

latitude = Latitude(degree = 22, minute = 54, second = 0)
j = 135 
latitude.set_hemisphere('S')
period = 1 #1 for a hour , 0.5 for half hour

# Solar Radiation Constants
a_s = 0.25
b_s = 0.50
# n = real duration of insolation
#  hours / numbers of day in period (month)
n = 220 / 31 # NOTE: It need to be changed based on each period and data information
# Short wave radiation
sigma = 0.23
# Long wave Radiation
stef_boltz=4.903e-9
tmax = 25.1 # C 
tmin = 19.1 # C
e_a = 2.1  #kPa

################################################

decimal_latitude = float(latitude.to_string('D'))
phi = math.radians(decimal_latitude)
dr = 1 + 0.033 *  math.cos(2 * math.pi * j / 365) 
ds = 0.409 * math.sin(2 * math.pi * j / 365 - 1.39)
ws = math.acos(-math.tan(phi) * math.tan(ds))

# Extraterrestrial radiation for daily periods (Ra) 
# Calculating  w ( The solar angle at the moment in which the midpoint of the considered period occurs )
b = ( 2 * math.pi * (j - 81) ) / 364
# seasonal correction for solar time.
sc = 0.1645 * math.sin(2 * b) * 0.1255 * math.cos(b) * 0.025 * math.sin(b)

# Gsc = 0,082 MJ m-2 min-1 ( solar constant )
# ra units MJ m-2 day-1.
ra = ((24 * 60) / math.pi) *  0.082  * ( (ws *  math.sin(phi) * math.sin(ds)) + (math.cos(phi) * math.cos(ds) * math.sin(ws)) )
print "Extraterrestrial radiation: %s MJ m-2 day-1" % str(ra)

# Solar Radiation
# rs units MJ m-2 day-1
N = 24 / math.pi * ws
rs = (a_s + b_s * ( n/N )) * ra

# Short wave radiation
#rns units MJ m-2 day 
rns = (1 - sigma) * rs
print "Short Wave radiation: %s MJ m-2 day-1" % str(rns)

# Long wave radiation
rso = (a_s + b_s) * ra
tmax_k = tmax + 273.15
tmin_k = tmin + 273.15
rnl = stef_boltz  * ((tmax_k ** 4+ tmin_k **  4) / 2) * (0.34 - 0.14 *  math.sqrt(e_a)) * (1.35 * (rs/rso) - 0.35)
print "Long Wave radiation: %s MJ m-2 day-1" % str(rnl)

# Net Radiation
rn = rns - rnl
print "Net radiation: %s MJ m-2 day-1" % str(rn)
