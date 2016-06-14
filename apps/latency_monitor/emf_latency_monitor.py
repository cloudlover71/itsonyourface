import ssl
import time
import socket
from urllib.parse import urlsplit

from emf_sdk import sender_factory, SENDER_TYPE


url = urlsplit('//localhost')
query = ('HEAD {path} HTTP/1.0\r\n'
         'Host: {hostname}\r\n'
         '\r\n').format(path=url.path or '/', hostname=url.hostname)

print("Query:", query)

while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.setblocking(True)
        sock.settimeout(3)
        sock = ssl.wrap_socket(sock, cert_reqs=ssl.CERT_NONE)
        sock.connect((url.hostname, 8004))
        print('Connected')

        sock.sendall(query.encode())
        data = sock.recv(1024).decode().split()
        print('Data received: {!r}'.format(data))

        #print("Ping: ", "OK" if data[1] == '200' else "-1")

        time.sleep(3)
    except socket.timeout:
        print('Timeout')
    except ConnectionError:
        pass
    except KeyboardInterrupt:
        print('Stopped')
        break
    finally:
        print('Socket closed')
        sock.close()
