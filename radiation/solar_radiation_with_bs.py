#!/usr/bin/python2.7
import argparse
import csv
import math
from calendar import monthrange
from dateutil import parser as dateparser
from LatLon import Latitude

parser = argparse.ArgumentParser()
parser.add_argument('--hemisphere', nargs='?', choices=['S','N'], help='Hemisphere identifier for latitudes must be N or S', required = True)
parser.add_argument('--data','-d', nargs='?' , help='File with isolation hours by month', required = True)
parser.add_argument('--latitude','-l', nargs='?' , help='Latitude in decimal format', required = True, type=float)

args = parser.parse_args()

################################################
#General functions

def get_day(month):
  return int(30.4 *  month - 15)

def get_number_of_days(month):
  return int(30.4 *  month - 15)

################################################

#Initial Variables

latitude = Latitude(args.latitude)
latitude.set_hemisphere(args.hemisphere)
period = 1 #1 for a hour , 0.5 for half hour

# Solar Radiation Constants
a_s = 0.25
b_s = 0.50
# n = real duration of insolation
#  isolation hours / numbers of day in period (month)
bs = 0
ev = 0
n = 0 # NOTE: It need to be changed based on each period and data information

# Short wave radiation
sigma = 0.23

# Long wave Radiation
stef_boltz = 4.903e-9
tmax = 0 # C
tmin = 0 # C
e_a = 0  #kPa

#Conversion Factors
KWH_M2_FACTOR = 0.2777777777777778

################################################
with open(str(args.data), "rb") as file_obj:
  reader = csv.DictReader(file_obj, delimiter=',')
  print "DATE,BS,RA,RS,RNS,RNL,RN"
  for row in reader:
    date = dateparser.parse(str(row["DATE"]))
    ndays = monthrange(date.year, date.month)[1]
    if row["BS"]:
      bs = float(row["BS"])
    if row["BS"] and row["DATE"]:
        n = bs / ndays
        j = get_day(date.month)
        if(row["TMAX"] and row["TMIN"]):
          tmax = float(row["TMAX"])
          tmin = float(row["TMIN"])
        if(row["TV"]):
          e_a = float(row["TV"])/10

        decimal_latitude = float(latitude.to_string('D'))
        phi = math.radians(decimal_latitude)

        dr = 1 + 0.033 *  math.cos(2 * math.pi * j / 365)
        ds = 0.409 * math.sin(2 * math.pi * j / 365 - 1.39)
        ws = math.acos(-math.tan(phi) * math.tan(ds))

        # cxtraterrestrial radiation for daily periods (Ra)
        # calculating  w ( The solar angle at the moment in which the midpoint of the considered period occurs )
        b = ( 2 * math.pi * (j - 81) ) / 364
        # seasonal correction for solar time.
        sc = 0.1645 * math.sin(2 * b) * 0.1255 * math.cos(b) * 0.025 * math.sin(b)

        # gsc = 0,082 MJ m-2 min-1 ( solar constant )
        # ra units MJ m-2 day-1.
        ra = ((24 * 60) / math.pi) *  0.082  * ( (ws *  math.sin(phi) * math.sin(ds)) + (math.cos(phi) * math.cos(ds) * math.sin(ws)) )
        # solar Radiation
        # rs units MJ m-2 day-1
        N = 24 / math.pi * ws
        rs = (a_s + b_s * ( n/N )) * ra
        # short wave radiation
        #rns units MJ m-2 day
        rns = (1 - sigma) * rs

        # long wave radiation
        rso = (a_s + b_s) * ra
        rnl = 0
        if(row["TMAX"] and row["TMIN"] and row["TV"]):
          tmax_k = tmax + 273.15
          tmin_k = tmin + 273.15
          rnl = stef_boltz  * ((tmax_k ** 4+ tmin_k **  4) / 2) * (0.34 - 0.14 *  math.sqrt(e_a)) * (1.35 * (rs/rso) - 0.35)

        # Net Radiation
        rn = rns - rnl

        #Changing units
        rs *= KWH_M2_FACTOR
        ra *= KWH_M2_FACTOR
        rns *= KWH_M2_FACTOR
        rnl *= KWH_M2_FACTOR
        rn *= KWH_M2_FACTOR
        print "%s,%s,%s,%s,%s,%s,%s" % (date, bs, ra, rs, rns, rnl, rn)
    else:
        a=1
        #print "%s" % (date)
