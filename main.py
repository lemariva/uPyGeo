#Copyright [2017] [Mauro Riva <lemariva@mail.com> <lemariva.com>]
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
#
#The above copyright notice and this permission notice shall be
#included in all copies or substantial portions of the Software.

import os
import time
import logging
import gc
from machine import RTC
from machine import SD
from geoposition import geolocate

gps_file = "gps.csv"
google_api_key = <GOOGLE_API_KEY>
position_interval = 5

gps_saved = 0
logger = logging.getLogger(__name__)

def setRTCLocalTime():
    rtc = RTC()
    rtc.ntp_sync("time1.google.com")
    time.sleep_ms(750)
    logger.info(' RTC Set from NTP to UTC: %s' % str(rtc.now()))
    #utime.timezone(-18000)
    #logger.info(' adjusted from UTC to EST timezone', utime.localtime(), '\n')

setRTCLocalTime()
actual_time = time.time()

# geo data and time
geo_locate = geolocate(google_api_key, ssid_)
geo_time = RTC()

# connecting the SD card
sd = SD()
time.sleep_ms(750)

try:
    os.mount(sd, '/sd')
except Exception as error:
    logger.error(str(error))
    pycom.rgbled(0xFFFF00)
    time.sleep_ms(2000)

while True:
    if(time.time() - actual_time >= position_interval):
        actual_time = time.time()
        logger.info(' opening file for GPS position - memory free: ' + str(gc.mem_free()))
        f = open('/sd/' + gps_file, 'a')
        try:
            pycom.rgbled(0x001100)
            time_now = geo_time.now()
            time_now_str = ','.join([str(x) for x in time_now])
            logger.info(' time got')
            valid, location = geo_locate.get_location()
            logger.info(' geo got')
            pycom.rgbled(0x005500)
            if(valid):
                f.write(time_now_str + "," + geo_locate.get_location_string())
                logger.info(' writing GPS position - number: ' + str(gps_saved))
                gps_saved = gps_saved + 1
                pycom.rgbled(0x00FF00)
            else:
                pycom.rgbled(0xFF00FF)
        except Exception as error:
            logger.error(str(error))
            pycom.rgbled(0xFFFF00)
            time.sleep_ms(2000)
        f.close()
    gc.collect()    # collector avoid memory leak?
    time.sleep_ms(2000)
    pycom.rgbled(0x050505)
