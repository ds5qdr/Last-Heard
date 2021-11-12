from datetime import datetime
from time     import time, sleep, localtime, strftime, gmtime
from datetime import date, datetime
from func_time import *

import os
os.system('cls')

# importing module
from   geopy.geocoders import Nominatim
from   timezonefinder  import TimezoneFinder
import pytz  
  
from   geopy.geocoders import Nominatim
from   timezonefinder  import TimezoneFinder
import pytz  
TZ_Log = 'tz-$(date -u +%Y-%m-%d.log)'
LOCAL_TIME = {}
last_date  = time_DATE()
last_cnt   = 0
def local_time(city_ctry, y) : 
    global last_date, last_cnt
    TIMEOUT = 5
    st_time = time()
    key     = ''
    tz = ''

    if city_ctry in LOCAL_TIME.keys() :
        Time_Zone = LOCAL_TIME[city_ctry]['TZ']
        key       = 'M' 
    else :   
        if   'Korea'  in city_ctry : Time_Zone = 'Asia/Seoul'   ; key = 'M'
        elif ',India' in city_ctry : Time_Zone = 'Asia/Kolkata' ; key = 'M'
        else :
            try : 
                city, ctry = city_ctry.split(',')            
                geolocator = Nominatim(user_agent="geoapiExercises") # initialize Nominatim API
                try :              
                    location   = geolocator.geocode(city_ctry, timeout=TIMEOUT)
                    Latitude   = location.latitude
                    Longitude  = location.longitude
                    key        = 'F'
                except :
                    location   = geolocator.geocode(ctry, timeout=TIMEOUT)
                    Latitude   = location.latitude
                    Longitude  = location.longitude
                    key        = 'S'
                time_zone = TimezoneFinder()
                Time_Zone = time_zone.timezone_at(lng=Longitude, lat=Latitude)
                # tz        = pytz.timezone(Time_Zone)         
                # Date      = datetime.now(tz)                                   
                # lc_time   = str(Date)[8:19]           
            except Exception as e : 
                print('--- local_time() error :' + e.__str__() )  
                Time_Zone = 'Asia/Seoul' 
                key       = 'E'
        LOCAL_TIME[city_ctry.strip()] = {'TZ':Time_Zone }
    cnt =  len(LOCAL_TIME)
    elap = str(time() - st_time)[:4] + key + str(len(LOCAL_TIME)).rjust(4,'-')
    line = time_DATE() + ' | ' + elap + ' | ' + str(y).rjust(7, '-') + ' | ' + Time_Zone + ' | ' + city_ctry

    if last_cnt != cnt :  
        last_cnt = cnt 
        print( line )

    ## city_ctry와 time_zone을 tz.txt에 저장 num = 22 매분, num = 19 매시
    num = 22
    if last_date[:num] != time_DATE()[:num] :
        with open('tz.txt', mode='w+',  encoding="utf-8") as open_file : 
            for city_ctry in LOCAL_TIME :
                line = city_ctry + '|' + LOCAL_TIME[city_ctry]['TZ']
                open_file.write(line + '\n')
            open_file.truncate() 
        last_date = time_DATE()
    return Time_Zone

with open('user.csv',  encoding="utf-8") as f:
    lines = f.readlines()
    y = 0
    for line in lines :
        dmrid, call, name1, name2,addr1, addr2, addr3 = line.split(',')
        address = addr2 + ',' + addr3.replace('\n', '')
        rtn = local_time(address, y)
        y += 1

