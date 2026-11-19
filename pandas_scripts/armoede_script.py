"""Clean the CBS 'Kerncijfers wijken en buurten 2022' (KWB) dataset into a poverty table per PC4."""

import pandas as pd

import excel_scripts
from excel_scripts import DATA_DIR

output_filename = "armoede_goed_2022.xlsx"

df = pd.read_excel(DATA_DIR / "kwb-2022-transformed-calculated.xlsx")

# Keep only municipality-level rows (drop district, neighbourhood and national rows)
column_name = "GWB_CODE_10"
substrings_to_delete = ["WK", "BU", "NL"]
df = excel_scripts.delete_rows_on_substrings_excel(df, column_name, substrings_to_delete)

df = excel_scripts.add_column(df, "jaartal", 2022)

df = excel_scripts.add_pc4_to_dataframe(
    df,
    DATA_DIR / "Locatie_codes.xlsx",
    locatie_code_column="GWB_CODE_10",
    locatie_dataset_code_column="GemCode",
)


def filter_columns_in_dataframe(df):
    columns_to_keep = [
        "jaartal",
        "PC4",
        "A_INW",
        "A_HH_M_K",
        "BEV_DICH",
        "G_WOZBAG",
        "G_INK_PI",
        "P_INK_HI",
        "G_HH_STI",
        "P_HH_LI",
        "A_SOZ_WW",
        "A_JZ_TN",
        "A_WMO_T",
        "G_PAU_HH",
        "STE_MVS",
        "STE_OAD",
    ]

    if not isinstance(df, pd.DataFrame):
        print("Fout: De invoer is geen pandas DataFrame.")
        return pd.DataFrame()  # Return an empty DataFrame on invalid input

    # Keep the columns that are both in the DataFrame and in 'columns_to_keep'
    return df[df.columns.intersection(columns_to_keep)].copy()


df = filter_columns_in_dataframe(df)

df = excel_scripts.rename_columns(df, {"PC4": "pc4_code"})
excel_scripts.turn_df_into_excel(df, output_filename)
