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

import time
import ujson
import requests
import logging
from network import WLAN

# https://developers.google.com/maps/documentation/geolocation/intro
# {
#   "homeMobileCountryCode": 310,
#   "homeMobileNetworkCode": 410,
#   "radioType": "gsm",
#   "carrier": "Vodafone",
#   "considerIp": "true",
#   "wifiAccessPoints": [
#     // See the WiFi Access Point Objects section below.
#   ]
# }

# // WiFi Access Point Objects
# {
#   "macAddress": "00:25:9c:cf:1c:ac",
#   "signalStrength": -43,
#   "age": 0,
#   "channel": 11,
#   "signalToNoiseRatio": 0
# }

# http://mcc-mnc.com/
logger = logging.getLogger(__name__)

class geolocate():
    def __init__(self, google_api_key, my_ssid, wlan_check_interval = 1, mcc=262, mnc=11):
        self.url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + google_api_key
        # wlan configuration and information
        self.wlan_scans = WLAN(mode=WLAN.STA)
        self.wlan_timer = 0
        self.wlan_check_interval = wlan_check_interval
        self.wlan_number = 0
        self.my_ssid = my_ssid
        self.nets = None
        self.rjson = None
        self.mcc = mcc
        self.mnc = mnc

    def prettify(self, mac_binary):
        return ':'.join('%02x' % (b) for b in mac_binary)

    def scan_wlan(self):
        logger.info(" wlan trying to scan")
        self.nets = self.wlan_scans.scan()
        self.wlan_timer = time.time()
        self.wlan_number = len(self.nets)
        logger.info(" wlan scan ready")

    def wlan_nodes(self):
        return self.wlan_number

    def get_location(self):
        valid = True
        if (self.nets == None) or (time.time()-self.wlan_timer >= self.wlan_check_interval):
            self.scan_wlan()

        # initializing the json request
        req = {}
        req["homeMobileCountryCode"] = self.mcc
        req["homeMobileNetworkCode"] = self.mnc
        req["radioType"] = "gsm"
        req["carrier"] = "O2"
        req["considerIp"] = "false"

        wlan_nodes = []
        for net in self.nets:
            if net.ssid != self.my_ssid:
                #print("ssid found: " + str(net.ssid) + " " + str(self.prettify(net.bssid)))
                wlan_node = {}
                wlan_node["macAddress"] = str(self.prettify(net.bssid))
                wlan_node["signalStrength"] = net.rssi
                wlan_node["channel"] = net.channel
                wlan_nodes.append(wlan_node)

        req["wifiAccessPoints"] = wlan_nodes

        try:
            r = requests.post(self.url, json=ujson.dumps(req))
            self.rjson = r.json()
        except Exception as error:
            logger.error(str(error))
            raise

        if (self.rjson.get("location") == None):
            print(self.rjson)
            valid = False

        return valid, self.rjson

    def get_location_string(self):
        location_string = None
        if (self.rjson.get("location") != None):
            location_string = str(self.rjson['location']['lat']) + "," + str(self.rjson['location']['lng']) + "," + str(self.rjson['accuracy']) + "\n"
        return location_string
