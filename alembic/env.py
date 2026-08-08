import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# ================== ДОБАВЛЯЕМ ИМПОРТЫ ==================
import sys
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Добавляем путь к корневой папке проекта
# Это нужно, чтобы Python нашел папку 'Python'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем ваш Base и модели
from Python.database.database import Base
from Python.database import models  # Важно: загружаем модели, чтобы Alembic их "увидел"
# ========================================================

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# ================== ФОРМИРУЕМ URL ИЗ .ENV ==================
# Получаем переменные из .env
db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "password")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "postgres")

# Формируем URL с помощью f-строки
database_url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Устанавливаем URL в конфиг Alembic
config.set_main_option("sqlalchemy.url", database_url)
# ==========================================================

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()