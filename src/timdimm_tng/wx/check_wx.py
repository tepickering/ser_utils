# -*- coding: utf-8 -*-

import astropy.units as u
from astropy.time import Time

from timdimm_tng.wx.salt_weather_xml import parse_salt_xml as salt_wx
from timdimm_tng.wx.lcogt_weather import get_weather as lcogt_wx
from timdimm_tng.wx.lcogt_bwc2_weather import get_weather as lcogt_bwc2_wx
from timdimm_tng.wx.gfz_weather import get_weather as gfz_wx


__all__ = ['get_current_conditions']


def get_current_conditions():
    """
    get the current weather conditions from the various weather stations
    """
    wx_dict = {}

    # get the current weather conditions from the SALT weather station
    wx_dict['SALT'] = salt_wx()

    # get the current weather conditions from the LCOGT weather station
    wx_dict['LCO'] = lcogt_wx()

    # get the current weather conditions from the LCOGT Boltwood weather station
    wx_dict['LCO_boltwood'] = lcogt_bwc2_wx()

    # get the current weather conditions from the GFZ weather station
    wx_dict['GFZ'] = gfz_wx()

    humidity = []
    precip = []
    wind = []
    for k, i in wx_dict.items():
        time_delt = Time.now() + 2 * u.hour - Time(i.get('TimeStamp_SAST'))
        if time_delt < 10 * u.min and i['Valid']:
            humidity.append(i['Rel_Hum'])
            precip.append(i['SkyCon'])
            wind.append(i['Wind_speed'])

    # make sure we have at least one weather station that has reported within 10 minues
    if len(humidity) > 0:
        # set humidity limit to 90%, precip to DRY for every sensor, and wind limit to 45 km/h
        humidity_check = all(rh < 90 for rh in humidity)
        precip_check = all(p == 'DRY' for p in precip)
        wind_check = all(w < 45 for w in wind)
        checks = [humidity_check, precip_check, wind_check]
    else:
        # if no weather station has reported within 10 minutes, then we have to close
        checks = [False]

    return wx_dict, checks