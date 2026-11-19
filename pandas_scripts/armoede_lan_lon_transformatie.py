"""Add latitude/longitude per PC4 code to the cleaned poverty (armoede) dataset."""

import pandas as pd

from excel_scripts import PROCESSED_DIR

kwb_df = pd.read_excel(PROCESSED_DIR / "armoede_goed_2022.xlsx")
loc_df = pd.read_excel(PROCESSED_DIR / "locatie_coords.xlsx")

merged_df = kwb_df.merge(
    loc_df[["pc4_code", "latitude", "longitude"]],
    on="pc4_code",
    how="left",  # keep all rows from the KWB table
)

merged_df.to_excel(PROCESSED_DIR / "kwb_2022_met_lat_lon_goed.xlsx", index=False)
