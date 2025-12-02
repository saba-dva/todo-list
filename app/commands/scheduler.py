import schedule
import time
import click
import os
import sys

def run_scheduler():
    """Run the scheduled task for auto-closing overdue tasks"""
    # Import inside function to avoid circular imports
    from app.commands.autoclose_overdue import autoclose_overdue_tasks
    
    interval = int(os.getenv('AUTOCLOSE_INTERVAL_MINUTES', 15))
    
    # Schedule the task
    schedule.every(interval).minutes.do(autoclose_overdue_tasks)
    
    click.echo(f"Scheduler started. Auto-closing overdue tasks every {interval} minutes.")
    click.echo("Press Ctrl+C to stop.")
    
    # Run once immediately
    click.echo("Running initial check...")
    autoclose_overdue_tasks()
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        click.echo("Scheduler stopped.")

def start_scheduler():
    """Start the scheduler for auto-closing overdue tasks"""
    run_scheduler()

if __name__ == '__main__':
    @click.command()
    def standalone_scheduler():
        start_scheduler()
    
    standalone_scheduler()
