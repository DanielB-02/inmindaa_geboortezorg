import pandas as pd
import excel_scripts as exs

dataset = "../data/Locatie_codes.xlsx"
df = pd.read_excel(dataset)

columns_to_remove = ['GemCode', 'GemNaam', 'WijkCode', 'Wijknaam', 'BuurtCode', 'Buurtnaam', 'PC6']
df = exs.remove_columns(df, columns_to_remove)

columns_with_duplicates = ['PC4']
df = exs.drop_duplicate_rows(df, columns_with_duplicates)

column_mapping = {'PC4': 'pc4_code', "Lokaliseringen van gemeenten/GGD-regio's/Code (code)": 'ggd_regio_code'}
df = exs.rename_columns(df, column_mapping)

exs.turn_df_into_excel(df, 'locatie.xlsx')