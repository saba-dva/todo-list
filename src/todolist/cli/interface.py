import click
from datetime import datetime
from typing import Optional

from ..core.entities.task import TaskStatus
from ..core.exceptions import ToDoListException
from ..storage.in_memory_storage import InMemoryStorage
from ..services.project_service import ProjectService
from ..services.task_service import TaskService


class ToDoListCLI:
    def __init__(self):
        self.storage = InMemoryStorage()
        self.project_service = ProjectService(self.storage)
        self.task_service = TaskService(self.storage, self.project_service)
    
    def display_error(self, message: str) -> None:
        click.echo(click.style(f"Error: {message}", fg='red'))
    
    def display_success(self, message: str) -> None:
        click.echo(click.style(f"Success: {message}", fg='green'))
    
    def display_info(self, message: str) -> None:
        click.echo(click.style(message, fg='blue'))
    
    def parse_date(self, date_str: str) -> Optional[datetime]:
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")


@click.group()
@click.pass_context
def cli(ctx):
    """ToDoList Application - Manage your projects and tasks"""
    ctx.obj = ToDoListCLI()


# Project commands
@cli.group()
def project():
    """Manage projects"""
    pass


@project.command()
@click.option('--name', prompt='Project name', help='Name of the project')
@click.option('--description', prompt='Project description', help='Description of the project')
@click.pass_obj
def create(todolist, name, description):
    """Create a new project"""
    try:
        project = todolist.project_service.create_project(name, description)
        todolist.display_success(f"Project '{project.name}' created with ID: {project.id}")
    except ToDoListException as e:
        todolist.display_error(str(e))


@project.command()
@click.pass_obj
def list(todolist):
    """List all projects"""
    projects = todolist.project_service.get_all_projects()
    if not projects:
        todolist.display_info("No projects found")
        return
    
    for project in projects:
        click.echo(f"ID: {project.id}")
        click.echo(f"Name: {project.name}")
        click.echo(f"Description: {project.description}")
        click.echo(f"Created: {project.created_at}")
        click.echo("-" * 40)


# Task commands would follow similar pattern...


if __name__ == '__main__':
    cli()