# Expedia-EMF-SDK

    Requires: Python 3.4.4+

## Project structure:
```
  | apps (Applications root folder)
  |- endpoint (Test Server)
  |- - ssl_keys (SSL key and certificate for HTTPS endpoint)
  |- - emf_endpoint.py (Application script)
  |- latency_monitor (Test Client)
  |- - latency_monitor.py (Application script)
  | emf_sdk (SDK module)
  |- helpers (Some internal helper functions
  |- messages (FluentD message object)
  |- senders (FluentD sender)
  | setup.py (SDK installer)
```

## FluentD default config:
```
    tag: emf.debug
    label: test
    host: localhost
    port: 24224
```

## SDK installation:
```
    cd apps/latency_monitor/
    pip install -r requirements.txt
```

## Applications running:
```
    Use "python application_script.py -h" for help. Example:
        python apps/latency_monitor/emf_latency_monitor.py -h
```

### Endpoint example:
```
    python apps/endpoint/emf_endpoint.py --host 127.0.0.1 --port 8004 --server-mode https --debug 1
```

### Latency monitor example:
```
    python apps/latency_monitor/emf_latency_monitor.py --host 127.0.0.1 --port 8004 --request_mode https --interval 3 --timeout 1 --debug 1
```
