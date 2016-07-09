import ssl
import time
import socket
import argparse
import configparser
from urllib.parse import urlsplit

from emf_sdk import get_logger, sender_factory, message_factory, SENDER_TYPE, REQUEST_TYPE, MESSAGE_TYPE, \
    METRIC_THRESHOLD_OPERATOR, METRIC_CALCULATION


parser = argparse.ArgumentParser(description='EMF SDK Latency Monitor')
parser.add_argument('--request-mode', type=str, required=True, choices=REQUEST_TYPE.get_list())
parser.add_argument('--host', type=str, required=True,
                    help='Target host. IP adress for TCP mode, URI without protocol and port for other modes')
parser.add_argument('--port', type=int, required=False, default=80, help='Target port')
parser.add_argument('--interval', type=int, required=True, help='Time interval in sec between requests')
parser.add_argument('--timeout', type=int, required=True,
                    help='Request timeout in sec. Notice that target host have its own timeout')

parser.add_argument('--sender-mode', type=str, required=True, choices=SENDER_TYPE.get_list())
parser.add_argument('--sender-label', type=str, required=True, help='Have diferent meaning depends on sender mode. '
                                                                    'For fluentd mode - label for multiple sources.')

parser.add_argument('--metric-threshold-operator', type=str, required=False,
                    default=METRIC_THRESHOLD_OPERATOR.GREATER_THAN, choices=METRIC_THRESHOLD_OPERATOR.get_list())
parser.add_argument('--metric-calculation', type=str, required=False,
                    default=METRIC_CALCULATION.AVERAGE, choices=METRIC_CALCULATION.get_list())

parser.add_argument('--source', type=str, required=False, default='EMFSDK', help='Default value EMFSDK')
parser.add_argument('--source-instance', type=str, required=False, default='BookingAPIMonitorInstance1',
                    help='Default value BookingAPIMonitorInstance1')

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
    try:
        header, _ = data.decode().split('\r\n', 1)
        return int(header.split()[1])
    except:
        return 0


if __name__ == '__main__':
    app_args = parser.parse_args()

    logger = get_logger('LatencyMonitorLogger', app_args.debug, app_args.log_file)

    config = configparser.ConfigParser()
    config.read('config.ini')

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

    message_cls = message_factory(MESSAGE_TYPE.LATENCY)
    sender = sender_factory(app_args.sender_mode, config[app_args.sender_mode])

    # Infinity loop. Stops by user or critical error
    while True:
        message = message_cls(host, app_args)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.setblocking(True)
        sock.settimeout(app_args.timeout)

        if app_args.request_mode == REQUEST_TYPE.HTTPS:
            sock = ssl.wrap_socket(sock, cert_reqs=ssl.CERT_NONE)

        # Connect to endpoint and calculate latency
        try:
            message.start()
            sock.connect((host, port))
            logger.debug('Connected to: %s:%s', host, port)

            # Check if connection was successful
            if app_args.request_mode in [REQUEST_TYPE.HTTP, REQUEST_TYPE.HTTPS]:
                sock.sendall(request_headers.encode())
                response_code = get_response_code(sock.recv(128))
                logger.debug('Response code: %s', response_code)

                if response_code == 200:
                    message.stop()
            else:
                message.stop()
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

        # Send message via sender
        try:
            sender.send(app_args.sender_label, message.as_dict())
            logger.debug('Message %s sent to %s' % (message.as_dict(), app_args.sender_mode))
        except Exception as e:
            logger.critical('Exception: %s', e)
            break

        # Wait for next iteration
        try:
            time.sleep(app_args.interval)
        except KeyboardInterrupt:
            logger.info('Stopped by user')
            break
