import pydantic_settings

from oss4x.src.config import SETTINGS


class Settings(pydantic_settings.BaseSettings):
    # For the indexes
    INDEXES_FOLDER: str = "indexes"


_S = Settings()

# Link to all documents
FILE_INPUT_INDEX = f"{_S.INDEXES_FOLDER}/repositories.toml"
FILE_INPUT_LISTINGS_INDEX = f"{_S.INDEXES_FOLDER}/listings.json"
FILE_OUTPUT_DIR = SETTINGS.LOCAL_FOLDER
FILE_OUTPUT_SUMMARY_TOML = f"{FILE_OUTPUT_DIR}/summary.toml"
