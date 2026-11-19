"""Clean the 2022 healthcare-supply dataset (distance to GP, hospital, etc.) per PC4."""

import pandas as pd

import excel_scripts
from excel_scripts import DATA_DIR

output_filename = "zorgaanbod_2022_obv_gemcode.xlsx"

df = pd.read_excel(DATA_DIR / "copy_zorgaanbod_2022.xlsx")

# Keep only municipality-level rows (drop district, neighbourhood and national rows)
column_name = "Codering_3"
substrings_to_delete = ["WK", "BU", "NL"]
df = excel_scripts.delete_rows_on_substrings_excel(df, column_name, substrings_to_delete)

df = excel_scripts.add_column(df, "jaartal", 2022)

df = excel_scripts.add_pc4_to_dataframe(
    df,
    DATA_DIR / "Locatie_codes.xlsx",
    locatie_code_column="Codering_3",
    locatie_dataset_code_column="GemCode",
)

columns_to_remove = [
    "Binnen5Km_12",
    "Codering_3",
    "Binnen3Km_7",
    "Binnen5Km_12",
    "Binnen10Km_13",
    "Binnen5Km_16",
    "Binnen10Km_17",
    "regio",
    "Binnen1Km_6",
]
df = excel_scripts.remove_columns(df, columns_to_remove)

column_mapping = {
    "PC4": "pc4_code",
    "AfstandTotHuisartsenpraktijk_5": "afstand_tot_huisartsenpraktijk",
    "Binnen5Km_8": "hpa_binnen_5km",
    "AfstandTotZiekenhuis_11": "afstand_tot_ziekenhuis_excl",
    "Binnen20Km_14": "ze_binnen_20km",
    "AfstandTotZiekenhuis_15": "afstand_tot_ziekenhuis_incl",
    "Binnen20Km_18": "zi_binnen_20km",
    "AfstandTotHuisartsenpost_9": "afstand_tot_huisartsenpost",
}
df = excel_scripts.rename_columns(df, column_mapping)

excel_scripts.turn_df_into_excel(df, output_filename)
