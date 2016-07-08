from azure.servicebus import ServiceBusService

from .base_sender import BaseSender


class EventHubConfig(object):
    service_namespace = None
    key_name = None
    key_value = None

    def __init__(self, params):
        self.service_namespace = params['service_namespace']
        self.key_name = params['key_name']
        self.key_value = params['key_value']


class EventHubSender(BaseSender):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sender = ServiceBusService(self._config.service_namespace,
                                         shared_access_key_name=self._config.key_name,
                                         shared_access_key_value=self._config.key_value)

    def send(self, label, data):
        assert isinstance(label, str), 'label must be a string'
        self._sender.send_event(label, data)
