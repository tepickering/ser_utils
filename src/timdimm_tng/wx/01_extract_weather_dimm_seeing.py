# -*- coding: utf-8 -*-
"""
Created on Fri 8 February 2019 at 12:00

@author: rbk

Get SALT weather data measurements from start date to end date specified
"""
import pandas as pd
from sqlalchemy import create_engine
import sys
import datetime

#date_start = "2017-01-01"
#date_end   = "2017-06-01"

date_start = str(sys.argv[1])
date_end   = str(sys.argv[2])

# date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d')
# date_start = date_start + datetime.timedelta(hours=12)

# date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d')
# date_end = date_end + datetime.timedelta(hours=12)

date_start = str(date_start)
date_end = str(date_end)

# ---------------------------------------------------------------------------------------------------------
# Getting and reading the seeing data from TimDim
# ---------------------------------------------------------------------------------------------------------
sys.stderr.write("\n Getting the data from the Suthweather database ...")
host = 'db.suth.saao.ac.za'
user = 'weatherreader'
passwd = 'weatherreader'
db = 'suthweather'
port = 3306

# sqlalchemy string format for DB connection
con = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(user,passwd,host,port,db)

# create a sqlalchemy engine
mysql_con = create_engine(con)

# do the query on the database
sql_query = 'SELECT datetime, sensor_datetime, temp, rel_hum, temp_dew, windsp, winddir, pressure FROM SALT' \
	  '       WHERE datetime >= \'{date_start}\' AND datetime < \'{date_end}\' ' \
	.format(date_start=date_start, date_end=date_end)
SALT_weather = pd.read_sql(sql_query, con=mysql_con)

# do the query on the database
sql_query = 'SELECT datetime, sensor_datetime, temp, rel_hum, temp_dew, windsp, winddir, pressure FROM LCOGT' \
	  '       WHERE datetime >= \'{date_start}\' AND datetime < \'{date_end}\' ' \
	.format(date_start=date_start, date_end=date_end)
LCOGT_weather = pd.read_sql(sql_query, con=mysql_con)

# do the query on the database
sql_query = 'SELECT datetime, sensor_datetime, temp, rel_hum, temp_dew, windsp, winddir, pressure FROM GFZ' \
	  '       WHERE datetime >= \'{date_start}\' AND datetime < \'{date_end}\' ' \
	.format(date_start=date_start, date_end=date_end)
GFZ_weather = pd.read_sql(sql_query, con=mysql_con)

# do the query on the database
sql_query = 'SELECT datetime, sensor_datetime, seeing FROM seeing' \
	  '       WHERE datetime >= \'{date_start}\' AND datetime < \'{date_end}\' ' \
	.format(date_start=date_start, date_end=date_end)
timdimm_seeing = pd.read_sql(sql_query, con=mysql_con)

# The seeing measurements on timdimm are zenith corrected. So the values are adjusted as if timdimm was pointing directly at the zenith.
# save the results to an output file
sys.stderr.write("\n Creating the output files ...")

SALT_filename = 'SALT_weather_data_'+date_start.split("-")[0]+'.csv'
sys.stderr.write("\n SALT Weather Data: %s \n" %SALT_filename)
SALT_weather.to_csv(SALT_filename, index = None )

LCOGT_filename = 'LCOGT_weather_data_'+date_start.split("-")[0]+'.csv'
sys.stderr.write("\n LCOGT Weather Data: %s \n" %LCOGT_filename)
LCOGT_weather.to_csv(LCOGT_filename, index = None )

GFZ_filename = 'GFZ_weather_data_'+date_start.split("-")[0]+'.csv'
sys.stderr.write("\n GFZ Weather Data: %s \n" %GFZ_filename)
GFZ_weather.to_csv(GFZ_filename, index = None )

DIMM_filename = 'DIMM_seeing_data_'+date_start.split("-")[0]+'.csv'
sys.stderr.write("\n DIMM Seeing Data: %s \n" %DIMM_filename)
timdimm_seeing.to_csv(DIMM_filename, index = None )

sys.stderr.write("\n Done")
sys.stderr.write("\n\n")

