"""
Main entry point for the ToDoList application.

NOTE (Deprecation):
-------------------
The CLI is deprecated. New development and all new features should be provided
through the FastAPI web API. The CLI will remain temporarily for backward compatibility,
but it is recommended to migrate clients to the API. See README.md -> "Deprecation Notice".
"""

import click
from dotenv import load_dotenv

load_dotenv()

DEPRECATION_MESSAGE = (
    "CLI interface is deceprated and will be removed in the next release. Please use the FastAPI HTTP interface instead."
)

@click.group()
def cli():
    click.echo(DEPRECATION_MESSAGE)
    """ToDoList App CLI + API"""
    pass

@cli.command("menu")
def menu():
    from app.cli.interface import main
    main()


@cli.command("close-overdue")
def close_overdue():
    from app.commands.autoclose_overdue import autoclose_overdue_tasks
    autoclose_overdue_tasks()


@cli.command("scheduler")
def scheduler():
    from app.commands.scheduler import start_scheduler
    start_scheduler()


@cli.command("init-db")
def init_db():
    from app.db.session import db_session
    db_session.create_tables()
    click.echo("Database initialized.")


@cli.command("api")
@click.option("--reload", is_flag=True)
def run_api(reload):
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=reload)


if __name__ == "__main__":
    print("CLI Deprecated: Please prefer the Web API (see README.md).")
    cli()