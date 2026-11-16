import os

from oss4x.scripts.src.config import FILE_OUTPUT_SUMMARY_TOML
from oss4x.src.log import log_info


def download_data():
    # Only triggered when actually needed (as it puts constraints on environment)
    from oss4x.app.src import data_io
    from oss4x.app.src.app_config import AppConfig
    from oss4x.app.src.config import (
        get_file_output_dir,
        get_file_output_listing_feather,
    )

    app_config = AppConfig()
    os.makedirs(get_file_output_dir(), exist_ok=True)
    for url_i, file_i in [
        (app_config.URL_RAW_INDEX, FILE_OUTPUT_SUMMARY_TOML),
        (app_config.URL_LISTING_FEATHER, get_file_output_listing_feather()),
    ]:
        if url_i is not None:
            data_io.download_file(url_i, file_i)

    log_info("Download complete")
