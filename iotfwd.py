
import requests

IOT_SERVER = 'http://roma3iot.adamantic.io:3000'
IOT_SERVER_SERVICE = IOT_SERVER + '/gisdata/temperature_humidity'

DEFAULT_COORDS = { # sligthly north of Appignano del Tronto, IT
    'X': 13.659000,
    'Y': 42.902000,
    'Z': 194
}

def build_payload(id, temp, hum, gpsnum, lat, lon, alt, ext = {}):        
    payload = {
        "sensorId" : id,
        "X"        : lon,
        "Y"        : lat,
        "Z"        : alt ,
        "t"        : temp,
        "h"        : hum
    }
    payload.update(ext)
    if gpsnum <= 0:
        payload.update(DEFAULT_COORDS)
    return payload

def send_to_iot_server(payload):
    r = requests.post(url=IOT_SERVER_SERVICE, data=payload)
    print('Sending to IOT server: status=', r.status_code, ', text=', r.text)
    return r.status_code == 200