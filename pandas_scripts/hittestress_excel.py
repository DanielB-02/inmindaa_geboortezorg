"""Clean the 2022 perceived-temperature (heat stress) dataset per PC4."""

import pandas as pd

from excel_scripts import DATA_DIR, add_column, remove_columns, rename_columns, turn_df_into_excel

# Configuration
file_path = DATA_DIR / "gevoelstemperatuurPC4_2022.xlsx"
columns_to_remove = [
    "fid",
    "fid_1",
    "buurtcode",
    "buurtnaam",
    "wijkcode",
    "gemeenteco",
    "gemeentena",
    "jrstatcode",
    "jaar",
]
column_mapping = {"PC4": "pc4_code"}
new_column_name = "jaartal"
new_column_value = 2022
output_filename = "hittestress_2022.xlsx"

# Processing
df = pd.read_excel(file_path)
df = remove_columns(df, columns_to_remove)
df = rename_columns(df, column_mapping)
df = add_column(df, new_column_name, new_column_value)
turn_df_into_excel(df, output_filename)
