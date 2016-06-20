import ssl
import asyncio
import argparse

from emf_sdk import get_logger, REQUEST_TYPE


parser = argparse.ArgumentParser(description='EMF SDK Endpoint')
parser.add_argument('--host', type=str, required=False)
parser.add_argument('--port', type=int, required=True)
parser.add_argument('--server-mode', type=str, required=True, choices=REQUEST_TYPE.get_list())
parser.add_argument('--debug', type=int, required=False, default=0, choices=[0, 1],
                    help='Set logging level to DEBUG and redirect output to STDOUT')
parser.add_argument('--log-file', type=str, required=False, default='emf_endpoint.log')


@asyncio.coroutine
def web_connection_handler(_, writer):
    logger.debug('Connection established %s', writer.get_extra_info('peername'))
    yield from writer.write('OK'.encode())
    writer.close()
    logger.debug('Connection closed %s', writer.get_extra_info('peername'))


@asyncio.coroutine
def tcp_connection_handler(_, writer):
    logger.debug('Connection established %s', writer.get_extra_info('peername'))
    yield from asyncio.sleep(3)  # TODO: Set timeout interval for abandoned connection
    writer.close()
    logger.debug('Connection closed %s', writer.get_extra_info('peername'))


if __name__ == '__main__':
    server_args = {}
    app_args = parser.parse_args()

    logger = get_logger('EMFEndpoint', app_args.debug, app_args.log_file)

    server_args['port'] = app_args.port
    if app_args.host:
        server_args['host'] = app_args.host

    if app_args.server_mode == REQUEST_TYPE.HTTPS:
        try:
            ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(certfile="ssl_keys/server.crt", keyfile="ssl_keys/server.key")
            server_args['ssl'] = ssl_context
        except FileNotFoundError:
            logger.critical('SSL keys is missing')
            exit()

    handle_connection = web_connection_handler if app_args.server_mode in [REQUEST_TYPE.HTTP, REQUEST_TYPE.HTTPS] \
                                               else tcp_connection_handler

    try:
        loop = asyncio.get_event_loop()
        server_gen = asyncio.start_server(handle_connection, **server_args)
        server = loop.run_until_complete(server_gen)
        logger.info('Server started in %s mode', app_args.server_mode)
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info('Server stopped by user')
    except Exception as e:
        logger.error('Exception: %s', e)
    finally:
        loop.close()
        logger.debug('Loop closed')
