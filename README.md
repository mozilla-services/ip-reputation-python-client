# ip-reputation-python-client

A Python client to the tigerblood IP reputation service

## Installation

`pip install ipreputation`


###  Usage:

Create a client:

```python
from ipreputation.client import IPReputationClient

client = IPReputationClient(
    hawk_id='<a hawk ID>',
	hawk_key='<a hawk key>',
	host='<tigerblood service IP address>',
	port='<tigerblood service port>',
	timeout=<float or int in seconds>)
```

Get the reputation for an IP:

```python
client.get('127.0.0.1').json()
```

Set the reputation for an IP:

```python
client.add('127.0.0.1', 70)
```

Update the reputation for an IP:

```python
client.update('127.0.0.1', 20)
```

Remove an IP:

```python
client.remove('127.0.0.1')
```

Send a violation for an IP:

```python
client.send_violation('127.0.0.1', 'rate-limit-exceeded')
```
