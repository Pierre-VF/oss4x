import os

from oss4climate_scripts.src.config import FILE_OUTPUT_SUMMARY_TOML
from oss4x.src.log import log_info


def download_data():
    # Only triggered when actually needed (as it puts constraints on environment)
    from oss4x.app.src import data_io
    from oss4x.app.src.config import (
        FILE_OUTPUT_DIR,
        FILE_OUTPUT_LISTING_FEATHER,
        URL_LISTING_FEATHER,
        URL_RAW_INDEX,
    )

    os.makedirs(FILE_OUTPUT_DIR, exist_ok=True)
    for url_i, file_i in [
        (URL_RAW_INDEX, FILE_OUTPUT_SUMMARY_TOML),
        (URL_LISTING_FEATHER, FILE_OUTPUT_LISTING_FEATHER),
    ]:
        data_io.download_file(url_i, file_i)

    log_info("Download complete")
