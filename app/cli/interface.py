import click
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from app.db.session import db_session
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.models.task import TaskStatus
from app.exceptions.base import ToDoListException

class ToDoListCLI:
    def __init__(self):
        self.db_session = db_session.get_session()
        self.project_service = ProjectService(self.db_session)
        self.task_service = TaskService(self.db_session)
    
    def __del__(self):
        if hasattr(self, 'db_session'):
            self.db_session.close()
    
    def display_error(self, message: str) -> None:
        click.echo(click.style(f"Error: {message}", fg='red'))
    
    def display_success(self, message: str) -> None:
        click.echo(click.style(f"Success: {message}", fg='green'))
    
    def display_info(self, message: str) -> None:
        click.echo(click.style(f"Info: {message}", fg='blue'))
    
    def clear_screen(self):
        click.clear()
    
    def show_header(self):
        self.clear_screen()
        click.echo(click.style("=" * 50, fg='cyan'))
        click.echo(click.style("TO-DO LIST MANAGER", fg='cyan', bold=True))
        click.echo(click.style("=" * 50, fg='cyan'))
        click.echo()
    
    def parse_date(self, date_str: str) -> Optional[datetime]:
        if not date_str or date_str.lower() == 'skip':
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD or type 'skip'")
    
    def choose_project_interactive(self, prompt_text: str = "Select project") -> int:
        """Let user choose a project from list"""
        projects = self.project_service.get_all_projects()
        if not projects:
            raise ToDoListException("No projects found. Please create a project first.")
        
        click.echo("\nAvailable Projects:")
        for i, project in enumerate(projects, 1):
            click.echo(f"  {i}. {project.name}")
        
        while True:
            try:
                choice = click.prompt(f"\n{prompt_text} (1-{len(projects)})", type=int)
                if 1 <= choice <= len(projects):
                    return projects[choice - 1].id
                else:
                    self.display_error(f"Please enter a number between 1 and {len(projects)}")
            except ValueError:
                self.display_error("Please enter a valid number")
    
    def choose_task_interactive(self, project_id: int, prompt_text: str = "Select task") -> int:
        """Let user choose a task from list"""
        tasks = self.task_service.get_project_tasks(project_id)
        if not tasks:
            raise ToDoListException("No tasks found in this project.")
        
        click.echo("\nAvailable Tasks:")
        for i, task in enumerate(tasks, 1):
            status_display = click.style(f"[{task.status.value}]", 
                                       fg='green' if task.status == TaskStatus.DONE else 
                                       'blue' if task.status == TaskStatus.DOING else 'yellow')
            click.echo(f"  {i}. {task.title} {status_display}")
        
        while True:
            try:
                choice = click.prompt(f"\n{prompt_text} (1-{len(tasks)})", type=int)
                if 1 <= choice <= len(tasks):
                    return tasks[choice - 1].id
                else:
                    self.display_error(f"Please enter a number between 1 and {len(tasks)}")
            except ValueError:
                self.display_error("Please enter a valid number")
    
    def create_project_menu(self):
        self.show_header()
        click.echo(click.style("CREATE NEW PROJECT", fg='green', bold=True))
        click.echo()
        
        name = click.prompt("Project name")
        description = click.prompt("Project description")
        
        try:
            project = self.project_service.create_project(name, description)
            self.display_success(f"Project '{project.name}' created successfully!")
            click.pause()
        except ToDoListException as e:
            self.display_error(str(e))
            click.pause()
    
    def list_projects_menu(self):
        self.show_header()
        click.echo(click.style("ALL PROJECTS", fg='blue', bold=True))
        click.echo()
        
        try:
            projects = self.project_service.get_all_projects()
            if not projects:
                self.display_info("No projects found. Create your first project!")
                click.pause()
                return
            
            for i, project in enumerate(projects, 1):
                click.echo(click.style(f"Project {i}: {project.name}", fg='yellow', bold=True))
                click.echo(f"  Description: {project.description}")
                click.echo(f"  ID: {project.id}")
                click.echo(f"  Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")
                click.echo("-" * 40)
            
            click.pause()
        except ToDoListException as e:
            self.display_error(str(e))
            click.pause()
    
    def edit_project_menu(self):
        self.show_header()
        click.echo(click.style("EDIT PROJECT", fg='magenta', bold=True))
        click.echo()
        
        try:
            project_id = self.choose_project_interactive("Choose project to edit")
            project = self.project_service.get_project(project_id)
            
            click.echo(f"\nCurrent project: {click.style(project.name, fg='yellow')}")
            click.echo(f"Current description: {project.description}")
            click.echo()
            
            # Get new values from user
            name = click.prompt("New project name", default=project.name)
            description = click.prompt("New project description", default=project.description)
            
            # Update the project
            updated_project = self.project_service.update_project(project_id, name, description)
            self.display_success(f"Project '{updated_project.name}' updated successfully!")
            
            click.pause()
            
        except ToDoListException as e:
            self.display_error(str(e))
            click.pause()
    
    def delete_project_menu(self):
        self.show_header()
        click.echo(click.style("DELETE PROJECT", fg='red', bold=True))
        click.echo()
        
        try:
            project_id = self.choose_project_interactive("Choose project to delete")
            project = self.project_service.get_project(project_id)
            
            # Show project tasks count for warning
            tasks = self.task_service.get_project_tasks(project_id)
            task_count = len(tasks)
            
            click.echo(f"\nProject to delete: {click.style(project.name, fg='yellow')}")
            click.echo(f"Description: {project.description}")
            click.echo(f"This project contains {task_count} task(s) that will also be deleted.")
            click.echo()
            
            if click.confirm("Are you sure you want to delete this project and all its tasks?"):
                self.project_service.delete_project(project_id)
                self.display_success("Project deleted successfully!")
            else:
                self.display_info("Deletion cancelled")
            
            click.pause()
            
        except ToDoListException as e:
            self.display_error(str(e))
            click.pause()
    
    def create_task_menu(self):
        self.show_header()
        click.echo(click.style("CREATE NEW TASK", fg='green', bold=True))
        click.echo()
        
        try:
            project_id = self.choose_project_interactive("Choose project for the task")
            project = self.project_service.get_project(project_id)
            
            click.echo(f"\nCreating task in project: {click.style(project.name, fg='yellow')}")
            title = click.prompt("Task title")
            description = click.prompt("Task description")
            deadline = click.prompt("Deadline (YYYY-MM-DD) or 'skip'", default='skip')
            
            deadline_date = self.parse_date(deadline)
            
            task = self.task_service.create_task(project_id, title, description, deadline_date)
            self.display_success(f"Task '{task.title}' created successfully!")
            click.pause()
            
        except ToDoListException as e:
            self.display_error(str(e))
            click.pause()
        except ValueError as e:
            self.display_error(str(e))
            click.pause()
    
    def list_tasks_menu(self):
        self.show_header()
        click.echo(click.style("PROJECT TASKS", fg='blue', bold=True))
        click.echo()
        
        try:
            project_id = self.choose_project_interactive("Choose project to view tasks")
            project = self.project_service.get_project(project_id)
            tasks = self.task_service.get_project_tasks(project_id)
            
            click.echo(f"\nTasks in project: {click.style(project.name, fg='yellow', bold=True)}")
            
            if not tasks:
                self.display_info("No tasks found in this project.")
                click.pause()
                return
            
            todo_count = len([t for t in tasks if t.status == TaskStatus.TODO])
            doing_count = len([t for t in tasks if t.status == TaskStatus.DOING])
            done_count = len([t for t in tasks if t.status == TaskStatus.DONE])
            
            click.echo(f"Summary: {click.style(f'{todo_count} TODO', fg='yellow')} | "
                      f"{click.style(f'{doing_count} DOING', fg='blue')} | "
                      f"{click.style(f'{done_count} DONE', fg='green')}")
            click.echo()
            
            for i, task in enumerate(tasks, 1):
                status_color = 'green' if task.status == TaskStatus.DONE else 'blue' if task.status == TaskStatus.DOING else 'yellow'
                
                click.echo(click.style(f"{i}. {task.title} [{task.status.value}]", fg=status_color, bold=True))
                click.echo(f"   Description: {task.description}")
                click.echo(f"   ID: {task.id}")
                click.echo(f"   Deadline: {task.deadline.strftime('%Y-%m-%d') if task.deadline else 'Not set'}")
                click.echo(f"   Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
                click.echo()
            
            click.pause()
            
        except ToDoListException as e:
            self.display_error(str(e))
            click.pause()
    
    def change_task_status_menu(self):
        self.show_header()
        click.echo(click.style("CHANGE TASK STATUS", fg='blue', bold=True))
        click.echo()
        
        try:
            project_id = self.choose_project_interactive("Choose project")
            task_id = self.choose_task_interactive(project_id, "Choose task to update")
            task = self.task_service.get_task(task_id)
            
            click.echo(f"\nCurrent task: {click.style(task.title, fg='yellow')}")
            click.echo(f"Current status: {click.style(task.status.value, fg='blue')}")
            click.echo()
            
            click.echo("Available statuses:")
            click.echo("1. " + click.style("TODO", fg='yellow'))
            click.echo("2. " + click.style("DOING", fg='blue')) 
            click.echo("3. " + click.style("DONE", fg='green'))
            
            status_choice = click.prompt("\nChoose new status (1-3)", type=int)
            status_map = {1: TaskStatus.TODO, 2: TaskStatus.DOING, 3: TaskStatus.DONE}
            
            if status_choice in status_map:
                new_status = status_map[status_choice]
                updated_task = self.task_service.update_task_status(task_id, new_status)
                self.display_success(f"Task status updated to: {new_status.value}")
            else:
                self.display_error("Invalid choice")
            
            click.pause()
            
        except ToDoListException as e:
            self.display_error(str(e))
            click.pause()
    
    def edit_task_menu(self):
        self.show_header()
        click.echo(click.style("EDIT TASK", fg='blue', bold=True))
        click.echo()
        
        try:
            project_id = self.choose_project_interactive("Choose project")
            task_id = self.choose_task_interactive(project_id, "Choose task to edit")
            task = self.task_service.get_task(task_id)
            
            click.echo(f"\nEditing task: {click.style(task.title, fg='yellow')}")
            click.echo()
            
            new_title = click.prompt("New title", default=task.title)
            new_description = click.prompt("New description", default=task.description)
            
            current_deadline = task.deadline.strftime('%Y-%m-%d') if task.deadline else 'Not set'
            new_deadline = click.prompt(f"New deadline (YYYY-MM-DD) or 'skip'", default='skip')
            
            click.echo("\nChoose new status:")
            click.echo("1. " + click.style("TODO", fg='yellow'))
            click.echo("2. " + click.style("DOING", fg='blue')) 
            click.echo("3. " + click.style("DONE", fg='green'))
            
            status_choice = click.prompt("New status (1-3)", type=int, default={
                TaskStatus.TODO: 1, 
                TaskStatus.DOING: 2, 
                TaskStatus.DONE: 3
            }[task.status])
            
            status_map = {1: TaskStatus.TODO, 2: TaskStatus.DOING, 3: TaskStatus.DONE}
            new_status = status_map.get(status_choice, task.status)
            deadline_date = self.parse_date(new_deadline)
            
            updated_task = self.task_service.update_task(
                task_id, new_title, new_description, deadline_date, new_status
            )
            self.display_success(f"Task '{updated_task.title}' updated successfully!")
            click.pause()
            
        except ToDoListException as e:
            self.display_error(str(e))
            click.pause()
        except ValueError as e:
            self.display_error(str(e))
            click.pause()
    
    def delete_task_menu(self):
        self.show_header()
        click.echo(click.style("DELETE TASK", fg='red', bold=True))
        click.echo()
        
        try:
            project_id = self.choose_project_interactive("Choose project")
            task_id = self.choose_task_interactive(project_id, "Choose task to delete")
            task = self.task_service.get_task(task_id)
            
            click.echo(f"\nTask to delete: {click.style(task.title, fg='yellow')}")
            click.echo(f"Description: {task.description}")
            click.echo(f"Status: {task.status.value}")
            click.echo()
            
            if click.confirm("Are you sure you want to delete this task?"):
                self.task_service.delete_task(task_id)
                self.display_success("Task deleted successfully!")
            else:
                self.display_info("Deletion cancelled")
            
            click.pause()
            
        except ToDoListException as e:
            self.display_error(str(e))
            click.pause()
    
    def show_main_menu(self):
        while True:
            self.show_header()
            
            # Show quick stats
            try:
                projects = self.project_service.get_all_projects()
                project_count = len(projects)
                
                total_tasks = 0
                todo_tasks = 0
                doing_tasks = 0
                done_tasks = 0
                
                for project in projects:
                    tasks = self.task_service.get_project_tasks(project.id)
                    total_tasks += len(tasks)
                    todo_tasks += len([t for t in tasks if t.status == TaskStatus.TODO])
                    doing_tasks += len([t for t in tasks if t.status == TaskStatus.DOING])
                    done_tasks += len([t for t in tasks if t.status == TaskStatus.DONE])
                
                click.echo(click.style("QUICK STATS", fg='cyan'))
                click.echo(f"   Projects: {project_count}")
                click.echo(f"   Total Tasks: {total_tasks}")
                click.echo(f"   TODO: {todo_tasks} | DOING: {doing_tasks} | DONE: {done_tasks}")
                click.echo()
                
            except ToDoListException:
                pass
            
            click.echo(click.style("MAIN MENU", fg='magenta', bold=True))
            click.echo()
            click.echo("1. Create Project")
            click.echo("2. List Projects") 
            click.echo("3. Edit Project")
            click.echo("4. Delete Project")
            click.echo("5. Create Task")
            click.echo("6. View Project Tasks")
            click.echo("7. Change Task Status")
            click.echo("8. Edit Task")
            click.echo("9. Delete Task")
            click.echo("0. Exit")
            click.echo()
            
            choice = click.prompt("Choose an option (0-9)", type=int)
            
            if choice == 0:
                self.show_header()
                self.display_success("Thank you for using To-Do List Manager!")
                break
            elif choice == 1:
                self.create_project_menu()
            elif choice == 2:
                self.list_projects_menu()
            elif choice == 3:
                self.edit_project_menu()
            elif choice == 4:
                self.delete_project_menu()
            elif choice == 5:
                self.create_task_menu()
            elif choice == 6:
                self.list_tasks_menu()
            elif choice == 7:
                self.change_task_status_menu()
            elif choice == 8:
                self.edit_task_menu()
            elif choice == 9:
                self.delete_task_menu()
            else:
                self.display_error("Invalid choice! Please try again.")
                click.pause()


def main():
    """Main entry point for the interactive menu"""
    cli = ToDoListCLI()
    cli.show_main_menu()


if __name__ == '__main__':
    main()