#!/usr/bin/python
import urllib2
import datetime

def get_seeing():
    #****************************************************************************************
    #Open up the GFZ weather pages and parse the html code from relevant weather info
    
    current_time = datetime.datetime.now()
    d={}
    
    try:
        page = urllib2.urlopen("http://seeing.suth.saao.ac.za/~massdimm/seeing.txt")
        
    except urllib2.URLError:
        d['Valid'] = False
        return d

    info = page.readlines()
    seeing = float(info[0].strip())

    # first check the seeing before continiung, if its more that 9'' then we deem
    # the measurement to be invalid
    if seeing > 9:
        d['Valid'] = False
        return d

    date = info[1].strip().split('T')[0]
    time = info[1].strip().split('T')[1].split('+')[0]

    tempdate = date.split('-')
    year = int(tempdate[0])
    month = int(tempdate[1])
    day = int(tempdate[2])
    
    temptime = time.split(':')
    hour = int(temptime[0])
    minute = int(temptime[1])
    sec = int(temptime[2])    
        
    seeing_time = datetime.datetime(year, month, day, hour, minute, sec)
    
    timediff = current_time - seeing_time
    print seeing_time, timediff.seconds
    if timediff.seconds > 300:
        d['Valid'] = False
    else:
        d['Valid'] = True
    
    d['seeing'] = seeing
    d['TimeStamp_SAST'] = seeing_time
    return d

    
if __name__ == "__main__":
    timdimm = get_seeing()
    
    print ""
    print "------------ timdimm Seeing Data ------------"
    print "TimeStamp (SAST) : ", timdimm['TimeStamp_SAST']
    print "Seeing           : ", timdimm['seeing']
    print "Valid            : ", timdimm['Valid']
    print

    
    
