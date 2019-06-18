import network
import modbus
import iotfwd

import pprint

IPLIST_FILENAME = 'iplist.conf'
MODBUS_TCP_PORT = 8899

def get_server_list():
    try:
        iplist = open(IPLIST_FILENAME).readlines()
        iplist = [ip.strip() for ip in iplist if ip.strip()]
        if not iplist: raise IOError('IP List is empty')
    except IOError as fnf:
        iplist = network.scan_for_tcp_port(MODBUS_TCP_PORT)
        with open(IPLIST_FILENAME, 'w') as f:
            f.writelines((ip + '\n' for ip in iplist))
    return iplist


def main():
    iplist = get_server_list()
    print('IP List: ', iplist)
    for ip in iplist:
        readings = modbus.get_ws10_readings(ip, MODBUS_TCP_PORT)
        print('Readings for ', ip, ':')
        pprint.pprint(readings)
        payload = iotfwd.build_payload(
            ip, readings['temperature'], readings['humidity'],
            readings['gpsnum'], readings['lat'], readings['lon'], readings['alt'])
        iotfwd.send_to_iot_server(payload)

if __name__ == "__main__":
    main()