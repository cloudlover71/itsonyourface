class BaseSender(object):
    def __init__(self, config):
        self._config = config

    def send(self, data):
        raise NotImplementedError
