"""Average the Leefbaarometer liveability scores per PC4 for 2022."""

import pandas as pd

import excel_scripts as exs

df = pd.read_excel(exs.DATA_DIR / "Leefbaarometer-scores-dataset.xlsx")

df = exs.remove_columns(df, ["bu_code", "bu_naam"])

# Drop all measurement years other than 2022
to_delete = ["2002", "2008", "2012", "2014", "2016", "2018", "2020"]
df = exs.delete_rows_on_substrings_excel(df, "jaar", to_delete)

df = exs.drop_duplicate_rows(df, ["lbm", "jaar", "PC4"])

df = df.groupby("PC4")["lbm"].mean().reset_index()

exs.add_column(df, "jaar", 2022)

column_mapping = {"PC4": "pc4_code", "lbm": "lbm_score", "jaar": "jaartal"}
df = exs.rename_columns(df, column_mapping)

exs.turn_df_into_excel(df, "leefbaarometer_2022.xlsx")
