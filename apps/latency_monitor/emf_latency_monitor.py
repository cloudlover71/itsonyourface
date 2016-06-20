import ssl
import time
import socket
import argparse
from urllib.parse import urlsplit

from emf_sdk import get_logger, sender_factory, SENDER_TYPE, REQUEST_TYPE


parser = argparse.ArgumentParser(description='EMF SDK Latency Monitor')
parser.add_argument('--request_mode', type=str, required=True, choices=REQUEST_TYPE.get_list())
parser.add_argument('--host', type=str, required=True,
                    help='Target host. IP adress for TCP mode, URI without protocol and port for other modes')
parser.add_argument('--port', type=int, required=False, default=80, help='Target port')
parser.add_argument('--interval', type=int, required=True, help='Time interval in sec between requests')
parser.add_argument('--timeout', type=int, required=True,
                    help='Request timeout in sec. Notice that target host have its own timeout')
parser.add_argument('--debug', type=int, required=False, default=0, choices=[0, 1],
                    help='Set logging level to DEBUG and redirect output to STDOUT')
parser.add_argument('--log-file', type=str, required=False, default='latency_monitor.log')


def render_request_headers(hostname, path):
    headers = ('HEAD {path} HTTP/1.0\r\n'
               'Host: {hostname}\r\n'
               '\r\n').format(hostname=hostname, path=path)
    logger.info("Request headers: %s", headers.split())
    return headers


def get_response_code(data):
    header, _ = data.decode().split('\r\n', 1)
    return int(header.split()[1])


if __name__ == '__main__':
    app_args = parser.parse_args()

    logger = get_logger('LatencyMonitorLogger', app_args.debug, app_args.log_file)

    try:
        if app_args.request_mode in [REQUEST_TYPE.HTTP, REQUEST_TYPE.HTTPS]:
            url = urlsplit('//' + app_args.host)
            request_headers = render_request_headers(url.hostname, url.path or '/')
            host = url.hostname
        else:
            host = app_args.host

        port = app_args.port
    except Exception as e:
        logger.error('Exception: %s', e)
        exit()

    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            sock.setblocking(True)
            sock.settimeout(app_args.timeout)

            if app_args.request_mode == REQUEST_TYPE.HTTPS:
                sock = ssl.wrap_socket(sock, cert_reqs=ssl.CERT_NONE)

            sock.connect((host, port))
            logger.debug('Connected to: %s:%s', host, port)

            if app_args.request_mode in [REQUEST_TYPE.HTTP, REQUEST_TYPE.HTTPS]:
                sock.sendall(request_headers.encode())

                response_code = get_response_code(sock.recv(128))
                logger.debug('Response code: %s', str(response_code))

            #print("Ping: ", "OK" if data[1] == '200' else "-1")

        except socket.timeout:
            logger.info('Timeout reached')
        except ConnectionError as e:
            logger.error('ConnectionError: %s', e)
        except KeyboardInterrupt:
            logger.info('Stopped by user')
            break
        except Exception as e:
            logger.critical('Exception: %s', e)
            break
        finally:
            logger.debug('Socket closed')
            sock.close()

        try:
            time.sleep(app_args.interval)
        except KeyboardInterrupt:
            logger.info('Stopped by user')
            break
