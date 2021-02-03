import click

from .site import Site

pass_site = click.make_pass_decorator(Site)


@click.command()
@pass_site
def new(site: Site):
    """Creates a new project"""
    site.create()


@click.group()
@click.option(
    "--project", type=click.Path(exists=False, file_okay=False, allow_dash=False)
)
@click.version_option()
@click.pass_context
def run(ctx, site):
    """
    +++ humber +++
    """
    ctx.obj = Site(path=site)


run.add_command(new)
