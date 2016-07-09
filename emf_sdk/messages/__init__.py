import time
import datetime

from ..helpers import ConstantsMixing

__all__ = (
    "MESSAGE_TYPE",
    "METRIC_THRESHOLD_OPERATOR",
    "METRIC_CALCULATION",
    "message_factory"
)


class MESSAGE_TYPE(ConstantsMixing):
    LATENCY = 'latency'


class METRIC_THRESHOLD_OPERATOR(ConstantsMixing):
    GREATER_THAN = 'GreaterThan'
    GREATER_THAN_OR_EQUAL_TO = 'GreaterThanOrEqualTo'
    LESS_THAN = 'LessThan'
    LESS_THAN_OR_EQUAL_TO = 'LessThanOrEqualTo'


class METRIC_CALCULATION(ConstantsMixing):
    AVERAGE = 'Average'
    MAXIMUM = 'Maximum'
    MINIMUM = 'Minimum'
    SUM = 'Sum'


class LatencyMessage(object):
    def __init__(self, hostname, args):
        self.Hostname = hostname
        self.TimeMeasured = str(datetime.datetime.now())
        self.MetricName = 'Network Latency'
        self.MetricData = -1
        self.MetricUnits = 'ms'
        self.MetricThreshold = args.timeout
        self.MetricThresholdOperator = args.metric_threshold_operator
        self.MetricCalculation = args.metric_calculation
        self.Source = args.source
        self.SourceInstance = args.source_instance
        self._start_time = None
        self._end_time = None

    def as_dict(self):
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}

    def start(self):
        self._start_time = time.time()

    def stop(self):
        self._end_time = time.time()
        if self._start_time and self._end_time and self._end_time > self._start_time:
            self.MetricData = (self._end_time - self._start_time) * 1000  # Convert to ms


def message_factory(message_type):
    if message_type not in MESSAGE_TYPE.get_list():
        raise Exception('Unknown message type')

    # TODO: Message factory implementation here
    return LatencyMessage
