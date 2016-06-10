from .exceptions import EMFSenderException
from .fluent_sender import FluentConfig, FluentSender


__all__ = (
    "SENDER_TYPE",
    "sender_factory"
)


class SENDER_TYPE:
    FLUENT = 'fluent'


def sender_factory(sender_type, params):
    if sender_type == SENDER_TYPE.FLUENT:
        config = FluentConfig(params)
        return FluentSender(config)
    else:
        raise EMFSenderException('Unknown sender type "%s"' % sender_type)
