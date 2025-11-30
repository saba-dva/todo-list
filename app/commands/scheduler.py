import schedule
import time
import click
from .autoclose_overdue import autoclose_overdue_tasks
import os

def run_scheduler():
    """Run the scheduled task for auto-closing overdue tasks"""
    interval = int(os.getenv('AUTOCLOSE_INTERVAL_MINUTES', 15))
    
    # Schedule the task
    schedule.every(interval).minutes.do(autoclose_overdue_tasks)
    
    click.echo(f"Scheduler started. Auto-closing overdue tasks every {interval} minutes.")
    click.echo("Press Ctrl+C to stop.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        click.echo("Scheduler stopped.")

@click.command()
def start_scheduler():
    """Start the scheduler for auto-closing overdue tasks"""
    run_scheduler()