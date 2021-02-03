import click

from .project import Project

pass_project = click.make_pass_decorator(Project)


@click.command()
@pass_project
def new(project: Project):
    """Creates a new project"""
    project.create()


@click.group()
@click.option(
    "--project", type=click.Path(exists=False, file_okay=False, allow_dash=False)
)
@click.version_option()
@click.pass_context
def run(ctx, project):
    """
    +++ humber +++
    """
    ctx.obj = Project(path=project)


run.add_command(new)
