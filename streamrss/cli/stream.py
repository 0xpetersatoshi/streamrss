import json
import click
from sseclient import SSEClient


@click.command()
def stream():
    messages = SSEClient('http://localhost:8000/stream')
    for msg in messages:
        print(json.dumps({"id": msg.id, "event": msg.event, "data": msg.data}))
