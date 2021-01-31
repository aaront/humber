import click

from .project import create


@click.command()
@click.argument(
    "path", type=click.Path(exists=False, file_okay=False, allow_dash=False)
)
def new(path: str):
    """Creates a new project"""
    create(path)


@click.group()
@click.version_option()
@click.pass_context
def run(ctx):
    """
    +++ humber +++
    """
    pass


run.add_command(new)
