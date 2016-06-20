import ssl
import asyncio
import argparse


parser = argparse.ArgumentParser(description='EMF SDK Endpoint')
parser.add_argument('--host', type=str, required=False)
parser.add_argument('--port', type=int, required=True)
parser.add_argument('--ssl-enabled', type=int, required=False, default=0, choices=[1, 0])


@asyncio.coroutine
def handle_connection(_, writer):
    writer.write('OK'.encode())


if __name__ == '__main__':
    server_args = {}
    endpoint_args = parser.parse_args()

    try:
        if endpoint_args.ssl_enabled:
            ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(certfile="ssl_keys/server.crt", keyfile="ssl_keys/server.key")
            server_args['ssl'] = ssl_context
        server_args['port'] = endpoint_args.port
        if endpoint_args.host:
            server_args['host'] = endpoint_args.host

    except FileNotFoundError:
        print('SSL keys is missing')
        exit()
    except Exception as e:
        print(e)
        exit()

    loop = asyncio.get_event_loop()

    try:
        server_gen = asyncio.start_server(handle_connection, **server_args)
        server = loop.run_until_complete(server_gen)
        loop.run_forever()
    except KeyboardInterrupt:
        print('Stopped')
    except Exception as e:
        print(e)
    finally:
        loop.close()
