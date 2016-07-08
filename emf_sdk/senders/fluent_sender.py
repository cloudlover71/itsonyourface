from fluent.sender import FluentSender as NativeFluentSender
from fluent import event

from .base_sender import BaseSender


class FluentConfig(object):
    tag = None
    host = None
    port = None

    def __init__(self, params):
        self.tag = params['tag']
        self.host = params['host']
        self.port = params['port']


class FluentSender(BaseSender):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sender = NativeFluentSender(self._config.tag, self._config.host, self._config.port)

    def send(self, label, data):
        assert isinstance(label, str), 'label must be a string'
        event.Event(label, data, sender=self._sender)
