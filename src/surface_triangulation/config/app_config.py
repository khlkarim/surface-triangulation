import os
import sys
from dataclasses import dataclass
from loguru import logger
from dotenv import load_dotenv
from threading import Lock
from typing import Literal
from pathlib import Path

# ---------------------------------------
# TYPES
# ---------------------------------------
Environment = Literal["dev", "test", "prod"]
BackendSolver = Literal["gurobi"]

# ---------------------------------------
# CONFIG SINGLETON
# ---------------------------------------
@dataclass(frozen=True)
class Config:
    """Application configuration (singleton)."""

    env: Environment
    app_name: str

    window_width: int
    window_height: int

    config_dialog_name: str
    config_dialog_width: int
    config_dialog_height: int

    backend_solver: BackendSolver

    _instance = None
    _lock = Lock()

    @classmethod
    def get_instance(cls) -> "Config":
        """Thread-safe lazy singleton accessor."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls._load()
        return cls._instance

    @classmethod
    def _load(cls) -> "Config":
        """Load values from environment (dotenv already applied)."""
        raw_env = os.getenv("ENV", "prod").lower()
        if raw_env not in ("dev", "test", "prod"):
            raise ValueError(f"Invalid ENV value: {raw_env}")
        
        backend_solver = os.getenv("BACKEND_SOLVER", "gurobi")
        if backend_solver not in ("gurobi",):
            raise ValueError(f"Invalid BACKEND_SOLVER value: {backend_solver}")

        return Config(
            env=raw_env,
            app_name=os.getenv("APP_NAME", "Surface Triangulation"),

            window_width=int(os.getenv("WINDOW_WIDTH", "1200")),
            window_height=int(os.getenv("WINDOW_HEIGHT", "600")),

            config_dialog_name=os.getenv("CONFIG_DIALOG_NAME", "Configure Triangulation Parameters"),
            config_dialog_width=int(os.getenv("CONFIG_DIALOG_WIDTH", "800")),
            config_dialog_height=int(os.getenv("CONFIG_DIALOG_HEIGHT", "800")),

            backend_solver=backend_solver,
        )

# ---------------------------------------
# LOGGER CONFIG
# ---------------------------------------
def configure_logger(env: Environment) -> None:
    logger.remove()

    logger.add(
        sys.stderr,
        level="DEBUG" if env == "dev" else "INFO",
        backtrace=True,
        diagnose=False,
    )

    logger.add(
        "logs/app.log",
        rotation="1 day",
        retention="7 days",
        compression="zip",
        level="DEBUG",
    )

# ---------------------------------------
# PUBLIC ENTRYPOINT
# ---------------------------------------

def load_environment_file():
    load_dotenv()
    raw_env = os.getenv("ENV", "prod").lower()

    env_files = {
        "dev": ".env.dev.local",
        "test": ".env.test.local",
        "prod": ".env.prod.local",
    }

    env_file = env_files.get(raw_env)
    if env_file is None:
        raise ValueError(f"Invalid ENV value: {raw_env}")

    load_dotenv(Path(env_file), override=True)

def configure_app() -> Config:
    load_environment_file()
    config = Config.get_instance()
    configure_logger(config.env)
    return config
