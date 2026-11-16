import os
from pathlib import Path
from urllib.parse import urlsplit

import pydantic_settings
from dotenv import load_dotenv
from sqlalchemy.engine import URL


class Settings(pydantic_settings.BaseSettings):
    # For scraping
    GITHUB_API_TOKEN: str | None = None
    GITLAB_ACCESS_TOKEN: str | None = None
    LOCAL_FOLDER: str = str(Path(__file__).parent.parent.parent.parent / ".data")
    SCRAPING_SQLITE_DB: str = "db.sqlite"

    # Database
    DATABASE_USERNAME: str | None = None
    DATABASE_PASSWORD: str | None = None
    DATABASE_HOST: str = "db.sqlite"
    DATABASE_NAME: str | None = None
    DATABASE_PORT: int | None = None

    # Repository database URL (SQLite or PostgreSQL)
    REPOS_DATABASE_URL: str = "sqlite:///.data/repos.sqlite"

    # Identifiants of FTP for export (scripts only)
    EXPORT_FTP_URL: str | None = None
    EXPORT_FTP_USER: str | None = None
    EXPORT_FTP_PASSWORD: str | None = None
    # App settings
    DATA_REFRESH_KEY: str | None = None
    SENTRY_DSN_URL: str | None = None

    # Typesense settings
    TYPESENSE_API_KEY: str | None = None
    TYPESENSE_HOST: str | None = None
    TYPESENSE_CONNECTION_TIMEOUT: int = 2

    # For data and usage analytics
    UMAMI_SITE_ID: str | None = None

    model_config = pydantic_settings.SettingsConfigDict(
        env_file_encoding="utf-8",
    )

    @property
    def typesense_config(self) -> dict[str, int | str]:
        """
        Get Typesense configuration from TYPESENSE_HOST environment variable

        :return: Dictionary containing host, port, and protocol for Typesense connection
        :raises EnvironmentError: If hostname, scheme, or port is missing from TYPESENSE_HOST
        """
        url = urlsplit(self.TYPESENSE_HOST)
        if url.hostname in [None, ""]:
            raise OSError("Hostname must be provided in TYPESENSE_HOST")
        if url.scheme in [None, ""]:
            raise OSError("Scheme (http/https) must be provided in TYPESENSE_HOST")
        if url.port in [None, ""]:
            raise OSError("Port must be provided in TYPESENSE_HOST")
        return {
            "host": url.hostname,
            "port": url.port,
            "protocol": url.scheme,
        }

    @property
    def path_scraping_sqlite_db(self) -> str:
        """
        Get the full path to the scraping SQLite database

        :return: Full path string to the scraping database
        """
        return f"{self.LOCAL_FOLDER}/{self.SCRAPING_SQLITE_DB}"

    @property
    def database_connection_string(self) -> str | URL:
        """
        Get the full database connection string

        :return: Full database connection string
        """

        if None not in {
            self.DATABASE_USERNAME,
            self.DATABASE_PASSWORD,
            self.DATABASE_PORT,
            self.DATABASE_NAME,
        }:
            out = URL.create(
                drivername="postgresql",
                username=self.DATABASE_USERNAME,
                password=self.DATABASE_PASSWORD,
                host=self.DATABASE_HOST,
                port=self.DATABASE_PORT,
                database=self.DATABASE_NAME,
            )
            # Postgres case
            # out = f"://{}:{quote()}@{}:{}/{}"
        else:
            # Sqlite case
            out = f"{self.LOCAL_FOLDER}/{self.DATABASE_HOST}"
            if not out.endswith(".sqlite"):
                raise ValueError("Env DATABASE_HOST should point to a SQLite database")
            db_folder, __ = os.path.split(out)
            os.makedirs(db_folder, exist_ok=True)
            out = "sqlite:///" + out
        return out


# Loading settings
load_dotenv(override=True)

SETTINGS = Settings()
