import click

from .site import Site

pass_site = click.make_pass_decorator(Site)


@click.command()
@click.option("--name", "-n", type=str, prompt="Site name")
@pass_site
def new(site: Site, name: str):
    """Creates a new project"""
    site.create(name)


@click.group()
@click.option(
    "--config",
    type=click.Path(exists=False, file_okay=True, dir_okay=False, allow_dash=False),
)
@click.version_option()
@click.pass_context
def run(ctx, config):
    """
    +++ humber +++
    """
    ctx.obj = Site(config_path=config)


run.add_command(new)
