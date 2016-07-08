from .exceptions import EMFSenderException
from .fluent_sender import FluentConfig, FluentSender
from .event_hub_sender import EventHubConfig, EventHubSender


__all__ = (
    "SENDER_TYPE",
    "sender_factory"
)


class SENDER_TYPE:
    FLUENTD = 'fluentd'
    EVENT_HUB = 'event_hub'

    @staticmethod
    def get_list():
        return [SENDER_TYPE.FLUENTD, SENDER_TYPE.EVENT_HUB]


def sender_factory(sender_type, config):
    if sender_type == SENDER_TYPE.FLUENTD:
        config = FluentConfig(config)
        return FluentSender(config)
    elif sender_type == SENDER_TYPE.EVENT_HUB:
        config = EventHubConfig(config)
        return EventHubSender(config)
    else:
        raise EMFSenderException('Unknown sender type "%s"' % sender_type)
