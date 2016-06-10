import time
import asyncio
import urllib


from emf_sdk import sender_factory, SENDER_TYPE


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
        print(time.time())

    def connection_made(self, transport):
        print('Connection made')
        print(time.time())
        transport.close()

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

loop = asyncio.get_event_loop()
coro = loop.create_connection(lambda: EchoClientProtocol(loop), '127.0.0.1', 8004)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()


@asyncio.coroutine
def print_http_headers(url):
    url = urllib.parse.urlsplit(url)
    if url.scheme == 'https':
        connect = asyncio.open_connection(url.hostname, 443, ssl=True)
    else:
        connect = asyncio.open_connection(url.hostname, 80)
    reader, writer = yield from connect
    query = ('HEAD {path} HTTP/1.0\r\n'
             'Host: {hostname}\r\n'
             '\r\n').format(path=url.path or '/', hostname=url.hostname)
    writer.write(query.encode('latin-1'))
    while True:
        line = yield from reader.readline()
        if not line:
            break
        line = line.decode('latin1').rstrip()
        if line:
            print('HTTP header> %s' % line)

    # Ignore the body, close the socket
    writer.close()

loop = asyncio.get_event_loop()
task = asyncio.ensure_future(print_http_headers('127.0.0.1'))
loop.run_until_complete(task)
loop.close()


params = {
    'tag': 'emf.debug',
    'host': 'localhost',
    'port': 24224,
}

sender = sender_factory(SENDER_TYPE.FLUENT, params)
sender.send('test_label', {
    'key1': 'val1',
    'key2': 'val2'
})
