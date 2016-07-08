import logging

from azure.servicebus import ServiceBusService


logging.basicConfig(level=logging.DEBUG)

service_namespace = 'emf-test-ns'
key_name = 'RootManageSharedAccessKey'  #'emf-test-perm'
key_value = 'mVbGPz2Q+12CSgzr+NQ3DDw6z5krxrRBjKIZ6ZM6EUE='  #'HutG49z7tyBXdH6ZmGae04YWZGVJa5CkZtYq2c95i/U='
sbs = ServiceBusService(service_namespace,
                        shared_access_key_name=key_name,
                        shared_access_key_value=key_value)

sbs.send_event('emf-test-eh', '{ "DeviceId":"dev-01", "Temperature":"38.0" }')
