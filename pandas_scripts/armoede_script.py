import pandas as pd
import excel_scripts

output_filename = 'armoede_goed_2022.xlsx'

file_path = '../data/kwb-2022-transformed-calculated.xlsx'
df = pd.read_excel(file_path)

column_name = 'GWB_CODE_10'
substrings_to_delete = ['WK', 'BU', 'NL']
# 'GM'
df = excel_scripts.delete_rows_on_substrings_excel(df, column_name, substrings_to_delete)

new_column_name = 'jaartal'
new_column_value = 2022
df = excel_scripts.add_column(df, new_column_name, new_column_value)

location_set = "../data/Locatie_codes.xlsx"
location_dataset_code_column = "GemCode"
target_location_column = "GWB_CODE_10"

df = excel_scripts.add_pc4_to_dataframe(
    df,
    location_set,
    target_location_column,
    location_dataset_code_column,
)

def filter_columns_in_dataframe(df):
    columns_to_keep = [
        "jaartal", "PC4", "A_INW", "A_HH_M_K", "BEV_DICH", "G_WOZBAG", "G_INK_PI", "P_INK_HI",
        "G_HH_STI", "P_HH_LI", "A_SOZ_WW", "A_JZ_TN", "A_WMO_T", "G_PAU_HH", "STE_MVS", "STE_OAD"
    ]

    if not isinstance(df, pd.DataFrame):
        print("Fout: De invoer is geen pandas DataFrame.")
        return pd.DataFrame()  # Retourneer een leeg DataFrame bij ongeldige invoer

    # Filter kolommen die in het DataFrame én in de lijst 'columns_to_keep' voorkomen
    filtered_df = df[df.columns.intersection(columns_to_keep)].copy()

    print("DataFrame succesvol gefilterd.")
    return filtered_df  # df = excel_scripts.remove_columns(df, columns_to_remove)


df = filter_columns_in_dataframe(df)

column_mapping = {'PC4': 'pc4_code'}
df = excel_scripts.rename_columns(df, column_mapping)
excel_scripts.turn_df_into_excel(df, output_filename)
