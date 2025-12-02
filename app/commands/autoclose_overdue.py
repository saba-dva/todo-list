import click
from app.db.session import db_session
from app.services.task_service import TaskService

def autoclose_overdue_tasks():
    """Automatically close overdue tasks"""
    session = db_session.get_session()
    try:
        task_service = TaskService(session)
        overdue_tasks = task_service.get_overdue_tasks()
        
        closed_count = 0
        for task in overdue_tasks:
            try:
                task_service.close_overdue_task(task.id)
                closed_count += 1
                click.echo(f"Closed overdue task: {task.title} (ID: {task.id})")
            except Exception as e:
                click.echo(f"Error closing task {task.id}: {str(e)}")
        
        if closed_count == 0:
            click.echo("No overdue tasks found")
        else:
            click.echo(f"Successfully closed {closed_count} overdue tasks")
        
    except Exception as e:
        click.echo(f"Error in autoclose process: {str(e)}")
        session.rollback()
    finally:
        session.close()

@click.command()
def autoclose_overdue():
    """Command to close overdue tasks"""
    autoclose_overdue_tasks()

if __name__ == '__main__':
    autoclose_overdue()