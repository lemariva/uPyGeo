# uPyGeo
Geolocation on WiPy 2.0 (MicroPython) without GPS Module, only WiFi


About this Repository
--------------
This code uses a WiPy2.0 and the <a href="https://developers.google.com/maps/documentation/geolocation/intro" target="_blank">Google Geolocation API</a> as a Geo-Datalogger without GPS.


Example
------------------------
```python
from geoposition import geolocate

ssid_ = <your ssid>  							#usually defined in your boot.py file
google_api_key = <API_KEY> 					  	#get from google
geo_locate = geolocate(google_api_key, ssid_)	#geo_locate object

valid, location = geo_locate.get_location()
if(valid):
	print("The geo position results: " + geo_locate.get_location_string())

```

The class initializer receives the following arguments

* `google_api_key`: Google API key that you get clicking on the link available <a href="https://goo.gl/hTU1sZ" target="_blank">here<i class="uk-icon-justify uk-icon-link"></i></a>;
* `wlan_check_interval`: It defines the wait time between checking for new WiFi signals (in seconds (default = 1));
* `mcc`: Mobile Country Codes (MCC) (default=262 -o2 Germany), you can find some values <a href="http://mcc-mnc.com/" target="_blank">here<i class="uk-icon-justify uk-icon-link"></i></a>;
* `mnc`: Mobile Network Codes (MNC) (default=11 -o2 Germany), same as `mcc`.


Changelog
-------------
Revision 0.1 (initial commit)

More Info
---------------
* [Tutorial](https://lemariva.com/blog/2017/11/micropython-wipy2-0-geolocalization-using-wlan) - available from 01.11.2017
* [Google Geolocation API](https://developers.google.com/maps/documentation/geolocation/intro)
