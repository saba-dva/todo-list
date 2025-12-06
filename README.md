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

### Deprecation Notice — CLI (Phase 3)

**Important:** From Phase 3 onwards the CLI is **deprecated**. That means:

- The CLI still exists and works for now, but **it's no longer the primary interface**.
- All new features will be implemented only via the **Web API (FastAPI)**.
- Users/developers are **recommended** to migrate to the Web API.
- The CLI will be fully removed in a future release.

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

### Using PostgreSQL

The application uses PostgreSQL by default. No additional setup is required. The database file todolist.db will be created automatically in the project directory.

Start PostgreSQL with Docker:

```bash
# 1. Start PostgreSQL with Docker
docker-compose up -d

# 2. Install dependencies
poetry install

# 3. Initialize database
poetry run python main.py init-db
```


### Running the Application

Method 1: Api Auto-Documentation
```bash
# Run the API
poetry run python main.py api-server
```

Visit: http://localhost:8000/docs

Method 2: Interactive Menu

```bash
# Start the interactive command-line interface
poetry run python main.py menu
```
Method 3: Individual Commands

```bash
# Show all available commands
poetry run python main.py --help

# Close overdue tasks manually
poetry run python main.py close-overdue

# Start the auto-closing scheduler
poetry run python main.py scheduler

# Initialize database tables
poetry run python main.py init-db

```