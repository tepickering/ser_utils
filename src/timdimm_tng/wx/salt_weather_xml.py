#! /usr/bin/python
# -*- coding: utf-8 -*-

from xml.dom import minidom
from xml.etree import ElementTree as ET
import time
import MySQLdb as ml
import socket
import urllib2
import xml.parsers.expat
import os
import datetime

def parse_salt_xml():
    tcs_mode = {'0':'OFF', '1':'INITIALISE', '2':'READY', '3':'SLEW', '4':'TRACK', '5':'GUIDE', '6':'MAINTENANCE', '7':'CALIBRATION', '8':'MAJOR FAULT', '9':'SHUTDOWN'}

    e = {}
    # read the xml page
    T = time.localtime()
    localtime = '%s/%s/%s %s:%s:%s ' %(T[0],T[1],T[2],T[3],T[4],T[5])
    TCS_URL = "http://192.168.4.6/xml/salt-tcs-icd.xml"

    try:
        sock = urllib2.urlopen(TCS_URL)
        out = open('tcs.xml', 'w')
        out.write(sock.read())
        out.close()

    except urllib2.URLError:
        e['Valid'] = False
        return e
    #try:
    dom = minidom.parse('tcs.xml')

    def getText(nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
                tc = rc[0].split()
                return '_'.join(tc)
            else:
                return ''.join(rc)
                
    # get all the clusters in the xml file
    maincluster = dom.getElementsByTagName('Cluster')

#    print maincluster
    # read through the clusters to get get the elements and append it
    # to the dictionary

    d = {}
    for Elements in maincluster:
        temp = Elements.getElementsByTagName('Name')[0]
        cl = getText(temp.childNodes)
        cluster_name =  cl.replace(' ','_')
        t = []
        # test whether the element is text or not
        for element in Elements.childNodes:
            if element.nodeType != element.TEXT_NODE:
                t.append(element)
        # read the Name and Val fields from the </DBL> <DBL> blocks
        for i in range(2,len(t)):

            x = t[i].getElementsByTagName('Name')[0]
            y =  t[i].getElementsByTagName('Val')[0]
            
            name = '%s__%s' %(cluster_name, getText(x.childNodes))
            val = '%s' %getText(y.childNodes)
#            print name,val
            if t[i].nodeName == 'EW':
                choice = t[i].getElementsByTagName('Choice')
                d[name] = getText(choice[int(val)].childNodes)
            else:
                d[name] = val
                
    e['bms_validity'] = int(d['bms_external_conditions__validity'])
    # if the bms data validity value is zero then return an valid = False

    if e['bms_validity'] != 511:
        e['Valid'] = False
        return e
    else:
        pass
    
    # if bms data is valid continue:
    e['DateTime'] = str(d['tcs_xml_time_info__timestamp'].replace('/','-'))
    e['Bar_Press'] = float(d['bms_external_conditions__Air_pressure']) * 10
    e['DewTemp'] = float(d['bms_external_conditions__Dewpoint'])
    e['Rel_Hum'] = float(d['bms_external_conditions__Rel_Humidity'])
    e['Wind_sp'] = float(d['bms_external_conditions__Wind_mag_10m']) * 3.6
    e['Wind_dir'] = float(d['bms_external_conditions__Wind_dir_10m'])
    e['Temp'] = float(d['bms_external_conditions__Temperatures'])
    e['Rain'] =  int(d['bms_external_conditions__Rain_detected'])

    TempDate = e['DateTime'].split('_')[0].split('-')
    Year = int(TempDate[0])
    Month = int(TempDate[1])
    Day = int(TempDate[2])
    TempTime = e['DateTime'].split('_')[1]
    Hours = int(TempTime.split(':')[0])
    Minutes = int(TempTime.split(':')[1])
    Seconds = int(round(float(TempTime.split(':')[2])))

    e['TimeStamp_SAST'] = datetime.datetime(Year, Month, Day, Hours, Minutes, Seconds)

    
    if e['Rain'] == 0:
        e['SkyCon'] = 'DRY'
    elif e['Rain'] == 1:
        e['SkyCon'] = 'RAIN'
    e['Valid'] = True
    
#    print e
    return e


if __name__ == "__main__":
    SALT = parse_salt_xml()
    
    if SALT['Valid']:
        print ""
        print "------------ SALT Weather Data ------------"
        print "TimeStamp (SAST) : ", SALT['TimeStamp_SAST']
        print "Sky Condition    : ", SALT['SkyCon']
        print "Wind Speed (km/h): ", SALT['Wind_sp']
        print "Wind Direction   : ", SALT['Wind_dir']
        print "Temperature      : ", SALT['Temp']
        print "Relative Humidity: ", SALT['Rel_Hum'], "%"
        print "T - T(dew)       : ", float(SALT['Temp']) - float(SALT['DewTemp']) 
        print "Barometric Press : ", SALT['Bar_Press']
        print ""
        print ""
        
    else:
        print 'Connection is down or information from BMS is invalid'
