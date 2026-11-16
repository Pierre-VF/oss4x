"""
Tests for the app configuration module (oss4x/app/src/config.py).

Covers the lazy file-output path getters (issue #3) and the removal of the
dead app.state config assignments in create_app() (issue #5).
"""

import pytest

from oss4x.app import create_app
from oss4x.app.src import config
from oss4x.app.src.app_config import AppConfig
from oss4x.src.config import SETTINGS as DEFAULT_SETTINGS
from oss4x.src.config import Settings


@pytest.fixture
def restore_app_config():
    """Save and restore the module-level config globals around a test so that
    mutating them here does not leak into other tests."""
    saved_app_config = config.APP_CONFIG
    saved_settings = config.SETTINGS
    yield
    config.APP_CONFIG = saved_app_config
    config.SETTINGS = saved_settings


def test_file_output_paths_default(restore_app_config):
    """The output path getters fall back to the default settings when no app
    has been created yet (SETTINGS is None)."""
    config.APP_CONFIG = None
    config.SETTINGS = None
    assert config.get_file_output_dir() == DEFAULT_SETTINGS.LOCAL_FOLDER
    assert (
        config.get_file_output_listing_feather()
        == f"{DEFAULT_SETTINGS.LOCAL_FOLDER}/listing_data.feather"
    )


def test_file_output_paths_reflect_custom_settings(restore_app_config):
    """Regression test for issue #3: the output paths must be computed lazily
    from the Settings instance passed to create_app(), not frozen at import
    time from the default settings."""
    custom = Settings(LOCAL_FOLDER="/tmp/oss4x_test_output")
    config.set_current_config(AppConfig(), custom)
    assert config.get_file_output_dir() == "/tmp/oss4x_test_output"
    assert (
        config.get_file_output_listing_feather()
        == "/tmp/oss4x_test_output/listing_data.feather"
    )


def test_app_state_does_not_expose_config(restore_app_config):
    """Regression test for issue #5: route handlers read config from the
    config module globals, not from app.state. The dead app.state.app_config /
    app.state.settings assignments in create_app() were removed."""
    app = create_app(AppConfig())
    assert not hasattr(app.state, "app_config")
    assert not hasattr(app.state, "settings")
