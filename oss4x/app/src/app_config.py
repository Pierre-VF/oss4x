"""
Application configuration for oss4x deployments.

This module defines the merged configuration that combines deployment-facing
settings and the theme into a single pydantic-validated model.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

from oss4x.app.src.theme import Theme


class AppConfig(BaseSettings):
    """
    Merged application configuration for a specific deployment.

    Combines deployment-facing settings (URLs, feature flags, paths)
    with the theme configuration. Use this to configure the app for
    a specific application case.
    """

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
    )

    # Deployment URLs
    APP_URL_BASE: str = ""
    APP_PROXY_PATH: str | None = None
    APP_URL_FAVICON: str | None = None
    URL_CODE_REPOSITORY: str = "https://github.com/Pierre-VF/oss4x"
    URL_FEEDBACK_FORM: str = ""
    URL_LISTINGS_INDEX: str = "https://raw.githubusercontent.com/Pierre-VF/oss4x/refs/heads/main/indexes/listings.json"
    URL_RAW_INDEX: str | None = None
    URL_LISTING_FEATHER: str | None = None
    FORCE_HTTPS: bool = True

    # Feature flags
    ENABLE_HYBRID_SEARCH: bool = False

    # Paths
    INDEXES_FOLDER: str = "indexes"
    FILE_INPUT_LISTINGS_INDEX: str = "indexes/listings.json"

    # Theme
    theme: Theme = Theme()

    @property
    def full_url_base(self) -> str:
        """
        Get the full URL base by combining APP_URL_BASE and APP_PROXY_PATH.

        :return: Combined URL base string
        """
        if (self.APP_PROXY_PATH is None) or (self.APP_PROXY_PATH == ""):
            return self.APP_URL_BASE
        else:
            return f"{self.APP_URL_BASE}{self.APP_PROXY_PATH}"
