import socket


def guess_own_ip():
    '''Guesses own IP.
    Tries to connect to Google's default DNS on port 80 and checks
    the IP of the selected network interface (according to OS routing).
    @return the IP of the current machine'''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

def split_ipv4(ipstr):
    '''Splits an IP in its components
    @return the integer parts of the ip'''
    return [int(s) for s in ipstr.split('.')]

def scan_for_tcp_port(port):
    split_ip = split_ipv4(guess_own_ip())
    own_term = split_ip.pop()
    found_list = []
    for term in range(1, 255):
        if term == own_term: continue
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            ip = '.'.join([str(t) for t in split_ip] + [str(term)])
            print ('Scanning IP ', {ip})
            s.connect((ip, port))
            found_list.append(ip)
        except (ConnectionError, OSError) as e:
            pass
        finally:
            s.close()
    return found_list
