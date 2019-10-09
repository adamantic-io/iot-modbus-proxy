import socket

from umodbus import conf
from umodbus.client import tcp


def get_ws10_readings(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
        message = tcp.read_input_registers(1, 0, 80)
        response = tcp.send_message(message, sock)
        payload = {
            'temperature': float(response[19]) / 10,
            'humidity': float(response[29]) / 10,
            'pressure': float(response[37]) / 10,
            'windspeed_kmh': float(response[49]) / 10,
            'wind_direction': float(response[54]) / 10,
            'precipitation': float(response[60]) / 100,
            'brightness': float(response[75]) / 10,
            'twilight': float(response[76]) / 10
        }
        message = tcp.read_input_registers(1, 140, 10)
        response = tcp.send_message(message, sock)
        payload.update({
            'lon': float(response[2]) / 10,
            'lat': float(response[3]) / 10,
            'alt': float(response[4]),
            'gpsnum': float(response[7]),
            'gpslock': float(response[8])
        })
        return payload
    finally:
        sock.close()
