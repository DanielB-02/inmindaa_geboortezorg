import pandas as pd
import excel_scripts as exs

dataset = "../data/Leefbaarometer-scores-dataset.xlsx"
df = pd.read_excel(dataset)

columns_to_remove = ['bu_code', 'bu_naam']
df = exs.remove_columns(df, columns_to_remove)

to_delete = ["2002", "2008", "2012", "2014", "2016", "2018", "2020"]
df = exs.delete_rows_on_substrings_excel(df, "jaar", to_delete)
print(df.head())

columns_with_duplicates = ['lbm', 'jaar', 'PC4']
df = exs.drop_duplicate_rows(df, columns_with_duplicates)
print(df.head())

df = df.groupby('PC4')['lbm'].mean().reset_index()

exs.add_column(df, 'jaar', 2022)

column_mapping = {'PC4': 'pc4_code', 'lbm': 'lbm_score', 'jaar': 'jaartal'}
df = exs.rename_columns(df, column_mapping)

exs.turn_df_into_excel(df, 'leefbaarometer_2022.xlsx')
