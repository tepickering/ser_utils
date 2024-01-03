# -*- coding: utf-8 -*-

import astropy.units as u
from astropy.time import Time

from timdimm_tng.wx.salt_weather_xml import parse_salt_xml as salt_wx
from timdimm_tng.wx.lcogt_weather import get_weather as lcogt_wx
#from timdimm_tng.wx.lcogt_bwc2_weather import get_weather as lcogt_bwc2_wx
from timdimm_tng.wx.gfz_weather import get_weather as gfz_wx
from timdimm_tng.wx.monet_weather import parse_monet as monet_wx


__all__ = ['get_current_conditions', 'WX_LIMITS']


# define operational weather limits for timdimm operation
WX_LIMITS = {
    'humidity': 90,
    'wind': 50,
    'temp': -5,
    'cloud': -20
}


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
    # wx_dict['LCO_boltwood'] = lcogt_bwc2_wx()

    # get the current weather conditions from the GFZ weather station
    wx_dict['GFZ'] = gfz_wx()

    # get the current weather conditions from the MONET weather station
    wx_dict['MONET'] = monet_wx()

    humidity = []
    precip = []
    wind = []
    temp = []
    cloud = []
    for _, i in wx_dict.items():
        time_delt = Time.now() + 2 * u.hour - Time(i.get('TimeStamp_SAST'))
        # only use data from the last 10 minutes
        if time_delt < 10 * u.min and i['Valid']:
            humidity.append(i['Rel_Hum'])
            precip.append(i['SkyCon'])
            wind.append(i['Wind_speed'])
            temp.append(i['Temp'])
            if 'Cloud' in i:
                cloud.append(i['Cloud'])

    # make sure we have at least one weather station that has reported within 10 minues
    if len(humidity) > 0:
        # set humidity limit to 90%, precip to DRY for every sensor,
        # wind limit to 50 km/h, and cloud limit to -20 C
        humidity_check = all(rh < WX_LIMITS['humidity'] for rh in humidity)
        precip_check = all(p == 'DRY' for p in precip)
        wind_check = all(w < WX_LIMITS['wind'] for w in wind)
        cloud_check = all(c < WX_LIMITS['cloud'] for c in cloud)
        temp_check = all(t > WX_LIMITS['temp'] for t in temp)
        checks = {
            'humidity': humidity_check,
            'precip': precip_check,
            'wind': wind_check,
            'temp': temp_check,
            'cloud': cloud_check,
            'monet': wx_dict['MONET']['Open']
        }
    else:
        # if no weather station has reported within 10 minutes, then we will have to close
        checks = None

    return wx_dict, checks


def main():
    wx_dict, checks = get_current_conditions()

    print("Weather Checks:")
    for k, v in checks.items():
        print(f"\t{k:15s}: {v}")

    for k, v in wx_dict.items():
        print(k)
        for k1, v1 in v.items():
            print(f"\t{k1:35s}: {v1}")


if __name__ == "__main__":
    main()