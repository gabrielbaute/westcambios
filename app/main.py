import uvicorn
import logging
import os

from app.config import Config
from app.api.app_factory import create_app
from app.database.db_config import init_db
from app.seeds import create_admin, create_rates


Config.create_dirs()
config = Config()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(Config.LOGS_PATH, "app.log"), encoding="utf-8"),
    ]    
)

app = create_app(config=config)
init_db(instance_path=Config.INSTANCE_PATH)

def run_server():
    """
    Run the FastAPI server.
    """
    uvicorn.run(
        "app.main:app",
        host=Config.API_HOST,
        port=Config.API_PORT,
        log_level="info",
        reload=False,
    )

if __name__ == "__main__":
    # Populate database
    create_admin()
    create_rates()

    # Run server
    run_server()