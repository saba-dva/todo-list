# ToDoList - Python OOP (In-Memory)

A Python-based ToDo List application built with Object-Oriented Programming principles and in-memory storage

##  Project Overview

This project implements a comprehensive task management system where users can create multiple projects and manage tasks within each project. 
###  Features

#### Project Management
-  Create new projects with name and description
-  List all projects with detailed information
-  Edit project name and description
-  Delete projects with cascade deletion of associated tasks
-  Unique project name validation
-  Character limit enforcement (30 chars for name, 150 for description)

#### Task Management
-  Create tasks within projects
-  Update task status (todo, doing, done)
-  Edit task details (title, description, deadline, status)
-  Delete tasks
-  List all tasks within a project
-  Deadline validation
-  Character limit enforcement (30 chars for title, 150 for description)

## How To Run
How to Run the ToDoList Application

### Prerequisites

Python 3.8.1 or higher
Poetry (dependency manager)
Docker (optional, for PostgreSQL)
Git
Installation

1. Clone the Repository

```bash
git clone <repository-url>
cd todo-list
```
2. Install Dependencies with Poetry

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```
3. Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your preferred editor
# The default uses SQLite, no additional setup required
```
### Running the Application

Method 1: Interactive Menu (Recommended)

```bash
# Start the interactive command-line interface
poetry run python main.py menu
```
Method 2: Individual Commands

```bash
# Show all available commands
poetry run python main.py --help

# Close overdue tasks manually
poetry run python main.py close-overdue

# Start the auto-closing scheduler
poetry run python main.py scheduler

# Initialize database tables
poetry run python main.py init-db

# Start the interactive menu
poetry run python main.py menu
Database Setup
```

### Using SQLite (Default, Easiest)

The application uses SQLite by default. No additional setup is required. The database file todolist.db will be created automatically in the project directory.

Using PostgreSQL (Optional)

If you prefer PostgreSQL:

Start PostgreSQL with Docker:

bash
docker-compose up -d
Update your .env file:

env
DATABASE_URL=postgresql://todolist_user:todolist_password@localhost:5432/todolist
Run database migrations:

bash
poetry run alembic upgrade head
