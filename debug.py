from emf_sdk import sender_factory, SENDER_TYPE


params = {
    'tag': 'emf.debug',
    'host': 'localhost',
    'port': 24224,
}

sender = sender_factory(SENDER_TYPE.FLUENT, params)
sender.send('test_label', {
    'key1': 'val1',
    'key2': 'val2'
})
