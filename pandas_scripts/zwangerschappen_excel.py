import pandas as pd
from excel_scripts import remove_columns, rename_columns, turn_df_into_excel, \
    drop_rows_from_column_with_null_values, strip_whitespace_from_column, add_pc4_to_excel

# Configuration
file_path = '../data/Ziekenhuisopnamen__ISHMT_en_regio_13062025_145613.xlsx'
columns_to_remove = ['Soort opname', 'Geslacht', 'Regio\'s', ]
column_mapping = {
    'Leeftijd': 'leeftijdsgroep',
    'Diagnose': 'diagnose',
    'Perioden': 'jaartal',
    'Opnamen per 10 000 inwoners (per 10 000 inwoners)': 'opnamen_per_1000_inwoners',
    'PC4': 'pc4_code'
                  }
column_with_null_values = 'opnamen_per_1000_inwoners'
# column_with_white_spaces = 'opnamen_per_1000_inwoners'
output_filename = 'zwangerschappen_2022.xlsx'


# Processing
df = pd.read_excel(file_path)
df = add_pc4_to_excel(df, '../data/Locatie_codes.xlsx', 'Regio\'s', 'GemNaam', 'zwangerschappen_2022.xlsx')
df = rename_columns(df, column_mapping)
df = remove_columns(df, columns_to_remove)
df = drop_rows_from_column_with_null_values(df, column_with_null_values)
# df = strip_whitespace_from_column(df, column_with_white_spaces)
turn_df_into_excel(df, output_filename)

# def add_pc4_to_excel(dataset, locatie_dataset, locatie_code_column, locatie_dataset_code_column, file_name):
#     """
#     Add PC4 codes to an Excel file
#     This will create new rows based on the combination of the location and PC4 codes
#     """
#     df = pd.read_excel(dataset)
#
#     ld_frame = pd.read_excel(locatie_dataset)
#     ld_frame = ld_frame[[locatie_dataset_code_column, "PC4"]]
#
#     df = pd.merge(df, ld_frame, left_on=[locatie_code_column], right_on=[locatie_dataset_code_column],
#                          how='left')
#
#     df.drop(columns=[locatie_dataset_code_column], inplace=True)
#     df = df.drop_duplicates()
#     df.to_excel(f"../bewerkte_data/{file_name}", index=False)
#
#     return df