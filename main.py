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

# Import FastAPI app for ASGI server
from api.app import app

load_dotenv()

DEPRECATION_MESSAGE = (
    "\nCLI Deprecated: Please prefer the Web API (see README.md).\n"
    "CLI interface is deprecated and will be removed in the next release. Please use the FastAPI HTTP interface instead."
)

@click.group()
def cli():
    click.echo(DEPRECATION_MESSAGE)
    """ToDoList App CLI + API"""
    pass

@cli.command("api-server")
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8000)
@click.option("--reload", is_flag=True)
def api_server(host, port, reload):
    import uvicorn
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
    )


@cli.command("menu")
def menu():
    from app.cli.interface import main
    main()


@cli.command("scheduler")
def scheduler():
    from app.commands.scheduler import start_scheduler
    start_scheduler()


@cli.command("close-overdue")
def close_overdue():
    from app.commands.autoclose_overdue import autoclose_overdue_tasks
    autoclose_overdue_tasks()


@cli.command("init-db")
def init_db():
    from app.db.session import db_session
    db_session.create_tables()
    click.echo("Database initialized.")


if __name__ == "__main__":
    cli()