import os
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    # App info
    APP_NAME: str = "WestCambios"
    APP_VERSIOM: str = "0.1.0"

    # Paths
    APP_PATH: Path = Path(__file__).resolve().parent.parent
    LOGS_PATH: Path = APP_PATH / "logs"
    INSTANCE_PATH: Path = APP_PATH / "instance"
    STATIC_PATH: Path = APP_PATH / "static"

    # Database
    DATABASE_URL: str = f"sqlite:///{os.path.join(INSTANCE_PATH, 'westcambios.db')}"
    DATABASE_CONNECT_ARGS: dict = {"check_same_thread": False}

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_ALLOW_ORIGINS: list = ["*"]
    API_ALLOW_METHODS: list = ["*"]
    API_ALLOW_HEADERS: list = ["*"]
    API_DEBUG: bool = True

    # Encryption
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    SECURITY_PASSWORD_SALT: str = os.getenv("SECURITY_PASSWORD_SALT")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7)

    @classmethod
    def create_dirs(cls) -> bool:
        """
        Creates the app directories

        Returns:
            bool: True if the directories were created, False otherwise
        """
        try: 
            cls.LOGS_PATH.mkdir(parents=True, exist_ok=True)
            cls.INSTANCE_PATH.mkdir(parents=True, exist_ok=True)
            cls.STATIC_PATH.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(e)
            return False
    
    @classmethod
    def get_app_paths(cls) -> Dict[str, Path]:
        """
        Returns the app paths

        Returns:
            Dict[str, Path]: The app paths
        """
        return {
            "app_path": cls.APP_PATH,
            "logs_path": cls.LOGS_PATH,
            "instance_path": cls.INSTANCE_PATH,
            "static_path": cls.STATIC_PATH
        }