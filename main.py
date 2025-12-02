#!/usr/bin/env python3
"""
Main entry point for the ToDoList application
"""

import click
import sys
import os
from dotenv import load_dotenv

# Load environment variables early
load_dotenv()

@click.group()
def cli():
    """ToDoList Application - Manage your projects and tasks"""
    pass

@cli.command(name='menu')
def menu_command():
    """Start the interactive menu"""
    try:
        from app.cli.interface import main as menu_main
        menu_main()
    except ImportError as e:
        click.echo(f"Error: {e}")
        click.echo("Make sure all dependencies are installed and modules exist")

@cli.command(name='close-overdue')
def close_overdue_command():
    """Close overdue tasks manually"""
    try:
        from app.commands.autoclose_overdue import autoclose_overdue_tasks
        autoclose_overdue_tasks()
    except ImportError as e:
        click.echo(f"Error: {e}")
        click.echo("Make sure the autoclose_overdue module exists")

@cli.command(name='scheduler')
def scheduler_command():
    """Start the scheduler for auto-closing overdue tasks"""
    try:
        from app.commands.scheduler import start_scheduler
        start_scheduler()
    except ImportError as e:
        click.echo(f"Error: {e}")
        click.echo("Make sure the scheduler module exists")

@cli.command(name='init-db')
def init_db_command():
    """Initialize database tables"""
    try:
        from app.db.session import db_session
        db_session.create_tables()
        click.echo("✓ Database tables created successfully!")
    except Exception as e:
        click.echo(f"✗ Error creating database tables: {e}")

if __name__ == '__main__':
    cli()