from pathlib import Path

import pandas as pd

from oss4x.app.src.config import get_file_output_listing_feather
from oss4x.src.database.projects import project_dataframe_loader

# Full indexing of the files
df: pd.DataFrame = project_dataframe_loader(get_file_output_listing_feather())

df_light = df[df["url"] == "https://github.com/Pierre-VF/oss4x"]
df_light["readme"] = df_light["readme"].apply(
    lambda x: x[:500].replace("\n", " ").replace(",", " ")
)

df_light.to_csv(str(Path(__file__).parent / "listing.csv"))
