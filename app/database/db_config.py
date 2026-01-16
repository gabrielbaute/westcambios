"""
Database initialization module
"""
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import Config
from app.database.db_base import Base

engine = create_engine(Config.DATABASE_URL, connect_args=Config.DATABASE_CONNECT_ARGS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db(instance_path: Path = Config.INSTANCE_PATH) -> None:
    """
    Initialize the database and creates the database directory

    Args:
        instance_path (Path): The path to the database instance directory
    """
    Path(instance_path).mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)