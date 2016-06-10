import asyncio


@asyncio.coroutine
def handle_connection(_, writer):
    writer.write('OK'.encode())

loop = asyncio.get_event_loop()

server_gen = asyncio.start_server(handle_connection, port=8004)
server = loop.run_until_complete(server_gen)

loop.run_forever()
loop.close()
