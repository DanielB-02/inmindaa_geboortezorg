"""Build the location dimension: one row per PC4 code with its GGD region."""

import pandas as pd

import excel_scripts as exs

df = pd.read_excel(exs.DATA_DIR / "Locatie_codes.xlsx")

columns_to_remove = ["GemCode", "GemNaam", "WijkCode", "Wijknaam", "BuurtCode", "Buurtnaam", "PC6"]
df = exs.remove_columns(df, columns_to_remove)

df = exs.drop_duplicate_rows(df, ["PC4"])

column_mapping = {"PC4": "pc4_code", "Lokaliseringen van gemeenten/GGD-regio's/Code (code)": "ggd_regio_code"}
df = exs.rename_columns(df, column_mapping)

exs.turn_df_into_excel(df, "locatie.xlsx")
