#!/usr/bin/env python3
"""
Main entry point for the ToDoList application
"""

import click
from app.cli.interface import main as menu_main
from app.commands.autoclose_overdue import autoclose_overdue
from app.commands.scheduler import start_scheduler

@click.group()
def cli():
    """ToDoList Application"""
    pass

@cli.command()
def menu():
    """Start the interactive menu"""
    menu_main()

@cli.command()
def close_overdue():
    """Close overdue tasks manually"""
    autoclose_overdue()

@cli.command()
def scheduler():
    """Start the scheduler for auto-closing overdue tasks"""
    start_scheduler()

if __name__ == '__main__':
    cli()