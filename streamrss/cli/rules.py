import json

import click
import requests
from streamrss.cli.constants import API_URL


URL = f"{API_URL}/stream/rules"

@click.group()
def rules():
    pass


@click.command()
def list():
    response = requests.get(URL)
    try:
        response.raise_for_status()
    except Exception as e:
        print(f"Error getting rules: {e}")

    rules = response.json()
    if len(rules["rules"]) == 0:
        print("no rules have been added yet!")
        return

    print(json.dumps(rules, indent=2))


@click.command()
@click.option("-p", "--pattern", type=str, required=True, help="The regex pattern to filter for")
@click.option("-t", "--tag", type=str, required=True, help="A nametag for the pattern")
def add(pattern, tag):
    response = requests.post(URL, json={"pattern": pattern, "tag": tag})
    try:
        response.raise_for_status()
    except Exception as e:
        print(f"Error creating rules: {e}")

    print("Rule successfully added")
    print(json.dumps(response.json(), indent=2))


rules.add_command(list, "list")
rules.add_command(add, "add")
