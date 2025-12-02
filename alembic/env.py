from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path so 'app' can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Load environment variables
load_dotenv()

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your models - use absolute import
try:
    # Try absolute import first
    from app.models.base import Base
    from app.models.project import Project
    from app.models.task import Task
    target_metadata = Base.metadata
    print("✓ Successfully imported models using absolute import")
except ImportError:
    try:
        # Try relative import as fallback
        from models.base import Base
        from models.project import Project  
        from models.task import Task
        target_metadata = Base.metadata
        print("✓ Successfully imported models using relative import")
    except ImportError as e:
        print(f"✗ Failed to import models: {e}")
        print("Current Python path:")
        for path in sys.path:
            print(f"  {path}")
        raise

def get_url():
    """Get database URL from environment or use default SQLite"""
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        return env_url
    else:
        # Default to SQLite
        return "sqlite:///todolist.db"

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    if configuration is None:
        configuration = {}
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()