import click
from streamrss.cli.rules import rules
from streamrss.cli.stream import stream


@click.group()
@click.version_option(version='0.1.0')
@click.pass_context
def cli(ctx):
    pass


cli.add_command(stream, "stream")
cli.add_command(rules, "rules")
