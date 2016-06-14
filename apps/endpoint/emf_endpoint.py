import ssl
import asyncio


sslcontext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
sslcontext.load_cert_chain(certfile="ssl_keys/server.crt", keyfile="ssl_keys/server.key")


@asyncio.coroutine
def handle_connection(_, writer):
    writer.write('OK'.encode())

loop = asyncio.get_event_loop()

server_gen = asyncio.start_server(handle_connection, port=8004, ssl=sslcontext)
server = loop.run_until_complete(server_gen)

loop.run_forever()
loop.close()
