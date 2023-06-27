#!/usr/bin/python
import MySQLdb as ml
import urllib2
import math
import datetime
import os, sys
import time
from BeautifulSoup import BeautifulSoup    
    
    
    
def open_page(sensor=0):
    '''
    open the LCOGT page for the BW cloud monitor. There are three and the 
    number specifies which one of the sensors to open
    '''    
    
    try:
        page = urllib2.urlopen("http://196.21.94.19:8080/RawttyUSB%i.txt"%sensor)
        info_string = page.readlines()[0].strip()
        page.close()
        
    except urllib2.URLError:
        info_string = 'None'        
        
    return info_string
    

def is_data(info_string):
    '''
    check whether the data pulled from the webpage is valid instrument data or
    calibration data.
    if check_char = 'D' then it is valid data
    '''
    #print info_string
    datetime = info_string.split(' : ')[0]
    data = info_string.split(' : ')[1].strip().split()
    
     # jpk 20130702: last check is to drop data where windsp = -2 and 
    # cloud =0. these values give false RAIN values and should not be 
    # recorded
    cloud_val = float(data[7])
    windsp_val = float(data[9])
    check_data = not (windsp_val == -2) and not (cloud_val < -500)
    
    
    check_char = data[0]
    
    if check_char == 'D' and check_data:
        
        return True, datetime, data
    
    else:
        return False, None, None        


def get_lcogt_bwc2_data(sensor=0):
    '''
    get the data from the website, but poll the website until we get valid data
    three tries to get the corrected data, otherwise return a False

    '''
    for i in [1,2,3]:
        info_string = open_page(sensor)
        valid, datetime, data = is_data(info_string)
        
        if valid == True:
            break
        else:
            time.sleep(3)
            
    return valid, datetime, data    
    
    
def get_weather():

    d = {}
    NowDate = datetime.date.today()    
    
    valid, BW_datetime, data = get_lcogt_bwc2_data(2)
    
    if valid == False:
        d['Valid'] = False
        return d
  
    else:
        
        DateNow = BW_datetime.split()[0]
        Year = int(DateNow[0:4])
        Month = int(DateNow[4:6])
        Day = int(DateNow[6:8])
        Time =  BW_datetime.split()[1]
        Hours = int(Time.split(':')[0])
        Minutes = int(Time.split(':')[1])
        Seconds = int(Time.split(':')[2])
        d['TimeStamp_SAST'] = datetime.datetime(Year, Month, Day, Hours, Minutes, Seconds)
        
        # the LCOGT time is in UT, have to add two hours to the sensor time
        d['TimeStamp_SAST'] = d['TimeStamp_SAST'] + datetime.timedelta(hours=2)
        
        d['Cloud'] = float(data[7])*1.45
        d['Temp'] = round(float(data[8]), 1)
        d['Wind_sp'] = round(float(data[9]), 0)
        Wet = data[10].strip()
        RainNow = data[11].strip()
        d['Rel_Hum'] = round(float(data[12]), 0)
        d['DewTemp'] = round(float(data[13]), 1)


        if (d['Cloud'] < -900.0) or (d['Cloud'] > 900.0):
            d['Cloud'] = 0
            
        if (RainNow == "r") or (RainNow == "R") or (Wet == "w") or (Wet == "W"):
            d['SkyCon'] = "RAIN"
        else:
            d['SkyCon'] = "DRY"
        
        
        d['Valid'] = True
        
        return d

if __name__ == "__main__":
    BWC2 = get_weather()
    
    print ""
    print "------------ BWC2 Weather Data ------------"
    print "TimeStamp (SAST) : ", BWC2['TimeStamp_SAST']
    print "Sky Condition    : ", BWC2['SkyCon']
    print "Wind Speed (km/h): ", BWC2['Wind_sp']
    print "Temperature      : ", BWC2['Temp']
    print "Relative Humidity: ", BWC2['Rel_Hum'], "%"
    print "T - T(dew)       : ", BWC2['Temp'] - BWC2['DewTemp']
    print "Cloud Cover      : ", BWC2['Cloud']


    print ""
    print ""
    

