import socket

from umodbus import conf
from umodbus.client import tcp


def get_ws10_readings(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        message = tcp.read_input_registers(1, 0, 80)
        response = tcp.send_message(message, sock)
        payload = {
            'temperature': response[19] / 10,
            'humidity': response[29] / 10,
            'pressure': response[37] / 10,
            'windspeed_kmh': response[49] / 10,
            'wind_direction': response[54] / 10,
            'precipitation': response[59] / 10,
            'brightness': response[75] / 10,
            'twilight': response[76] / 10,
        }
        message = tcp.read_input_registers(1, 140, 10)
        response = tcp.send_message(message, sock)
        payload.update({
            'lon': response[2] / 100,
            'lat': response[3] / 10,
            'alt': response[4],
            'gpsnum': response[7],
            'gpslock': response[8]
        })
        return payload
