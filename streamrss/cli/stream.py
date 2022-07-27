import json

import click
from sseclient import SSEClient
from streamrss.cli.constants import API_URL


@click.command()
def stream():
    messages = SSEClient(f"{API_URL}/stream")
    for msg in messages:
        print(json.dumps({"id": msg.id, "event": msg.event, "data": msg.data}))
