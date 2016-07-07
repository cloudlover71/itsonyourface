from azure.servicebus import ServiceBusService

service_namespace = 'emf-test-ns'
key_name = 'RootManageSharedAccessKey'
key_value = 'mVbGPz2Q+12CSgzr+NQ3DDw6z5krxrRBjKIZ6ZM6EUE='
sbs = ServiceBusService(service_namespace,
                        shared_access_key_name=key_name,
                        shared_access_key_value=key_value)

sbs.send_event('emf-test-eh', '{ "DeviceId":"dev-01", "Temperature":"37.0" }')

