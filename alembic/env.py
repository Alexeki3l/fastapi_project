from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine
from alembic import context
from dotenv import load_dotenv

# Carga variables de entorno del .env
load_dotenv()

# Importa tus modelos
from app.models.user import Base

# Configuración Alembic
config = context.config

# Obtiene la URL de la base de datos desde el .env
DATABASE_URL = os.getenv("DATABASE_URL")
# Convierte a URL síncrona para Alembic (psycopg)
if DATABASE_URL.startswith("postgresql+asyncpg://"):
    DATABASE_URL_SYNC = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql+psycopg://")
else:
    DATABASE_URL_SYNC = DATABASE_URL

config.set_main_option("sqlalchemy.url", DATABASE_URL_SYNC)

# Logger
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(config.get_main_option("sqlalchemy.url"))

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
