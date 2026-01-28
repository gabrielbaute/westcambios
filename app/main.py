import uvicorn
import logging
import os

from app.config import Config
from app.api.app_factory import create_app
from app.database.db_config import init_db
from app.seeds import create_admin, create_rates, create_rates_production
from app.services import SchedulerService


Config.create_dirs()
config = Config()

logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(Config.LOGS_PATH, "app.log"), encoding="utf-8"),
    ]    
)

app = create_app(config=config)
init_db(instance_path=Config.INSTANCE_PATH)

if Config.LOG_LEVEL.upper() == "DEBUG":
    create_admin()
    create_rates_production()

@app.on_event("startup")
def start_scheduler():
    """
    Start the scheduler.
    """
    scheduler = SchedulerService()
    scheduler.start_scheduler()


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
    run_server()