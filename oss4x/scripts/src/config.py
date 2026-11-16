from oss4x.app.src.config import AppConfig
from oss4x.src.config import SETTINGS

# Link to all documents
INDEXES_FOLDER = AppConfig().INDEXES_FOLDER
FILE_INPUT_INDEX = f"{INDEXES_FOLDER}/repositories.toml"
FILE_INPUT_LISTINGS_INDEX = f"{INDEXES_FOLDER}/listings.json"
FILE_OUTPUT_DIR = SETTINGS.LOCAL_FOLDER
FILE_OUTPUT_SUMMARY_TOML = f"{FILE_OUTPUT_DIR}/summary.toml"
