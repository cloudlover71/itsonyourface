from .senders import *
from .helpers import get_logger


class REQUEST_TYPE(object):
    TCP = 'tcp'
    HTTP = 'http'
    HTTPS = 'https'

    @staticmethod
    def get_list():
        return [REQUEST_TYPE.TCP, REQUEST_TYPE.HTTP, REQUEST_TYPE.HTTPS]
