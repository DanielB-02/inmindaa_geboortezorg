"""Clean the CBS hospital-admissions dataset (pregnancy-related, per municipality) and map it to PC4."""

import pandas as pd

from excel_scripts import (
    DATA_DIR,
    add_pc4_to_dataframe,
    drop_rows_from_column_with_null_values,
    remove_columns,
    rename_columns,
    turn_df_into_excel,
)

# Configuration
# Source file is not included in the repo; download it from CBS StatLine (see README).
file_path = DATA_DIR / "Ziekenhuisopnamen__ISHMT_en_regio_13062025_145613.xlsx"
columns_to_remove = ["Soort opname", "Geslacht", "Regio's"]
column_mapping = {
    "Leeftijd": "leeftijdsgroep",
    "Diagnose": "diagnose",
    "Perioden": "jaartal",
    "Opnamen per 10 000 inwoners (per 10 000 inwoners)": "opnamen_per_1000_inwoners",
    "PC4": "pc4_code",
}
column_with_null_values = "opnamen_per_1000_inwoners"
output_filename = "zwangerschappen_2022.xlsx"


# Processing
df = pd.read_excel(file_path)
df = add_pc4_to_dataframe(df, DATA_DIR / "Locatie_codes.xlsx", "Regio's", "GemNaam")
df = rename_columns(df, column_mapping)
df = remove_columns(df, columns_to_remove)
df = drop_rows_from_column_with_null_values(df, column_with_null_values)
turn_df_into_excel(df, output_filename)
