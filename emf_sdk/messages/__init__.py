import time
import datetime


__all__ = (
    "MESSAGE_TYPE",
    "message_factory"
)

class MESSAGE_TYPE(object):
    LATENCY = 'latency'

    @staticmethod
    def get_list():
        return [MESSAGE_TYPE.LATENCY]


class LatencyMessage(object):
    def __init__(self, hostname, timeout):
        self.Hostname = hostname
        self.TimeMeasured = str(datetime.datetime.now())
        self.MetricName = 'Network Latency'
        self.MetricData = -1
        self.MetricUnits = 'ms'
        self.MetricThreshold = timeout
        self.MetricThresholdOperator = 'GreaterThan'  # GreaterThan, GreaterThanOrEqualTo, LessThan, LessThanOrEqualTo
        self.MetricCalculation = 'Average'  # Average, Maximum, Minimum, Sum
        self.Source = 'EMFSDK'
        self.SourceInstance = 'BookingAPIMonitorInstance1'
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
