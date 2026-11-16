"""
Module-level configuration access for the oss4x app.

The current AppConfig and Settings instances are set by the create_app() factory.
Static paths and computed values are defined here.
"""

import importlib
import pathlib

from oss4x.app.src.app_config import AppConfig
from oss4x.src.config import SETTINGS as _DEFAULT_SETTINGS
from oss4x.src.config import Settings

_script_dir = pathlib.Path(__file__).resolve().parent.parent
TEMPLATES_PATH = _script_dir / "templates"
STATIC_FILES_PATH = _script_dir / "static"

# To prevent caching between versions (this doesn't work too well across instances, but does the job for now)
APP_VERSION = importlib.metadata.version("oss4x")

# Computed from Settings (infrastructure)
FILE_OUTPUT_DIR = _DEFAULT_SETTINGS.LOCAL_FOLDER
FILE_OUTPUT_LISTING_FEATHER = f"{FILE_OUTPUT_DIR}/listing_data.feather"

# Current config instances (set by create_app factory)
APP_CONFIG: AppConfig | None = None
SETTINGS: Settings | None = None


def set_current_config(app_config: AppConfig, settings: Settings | None = None) -> None:
    """Set the current config instances. Called by create_app()."""
    global APP_CONFIG, SETTINGS
    APP_CONFIG = app_config
    SETTINGS = settings or _DEFAULT_SETTINGS


def get_app_config() -> AppConfig:
    """Return the current AppConfig, raising a clear error if not yet set."""
    if APP_CONFIG is None:
        raise RuntimeError("create_app() has not been called. APP_CONFIG is not set.")
    return APP_CONFIG
