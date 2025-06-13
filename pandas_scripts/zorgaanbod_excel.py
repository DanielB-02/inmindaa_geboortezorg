import pandas as pd
import excel_scripts

file_path = "../data/old_zorgaanbod_2022.xlsx"
new_column_name = 'jaartal'
new_column_value = 2022
output_filename = 'zorgaanbod_2022.xlsx'
df = pd.read_excel(file_path)
df = excel_scripts.add_column(df, new_column_name, new_column_value)
excel_scripts.turn_df_into_excel(df, output_filename)