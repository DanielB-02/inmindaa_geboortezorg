import pandas as pd
import excel_scripts

file_path = "../bewerkte_data/zorgaanbod_2022.xlsx"
new_column_name = 'jaartal'
new_column_value = 2022
output_filename = 'zorgaanbod_2022.xlsx'


columns_to_remove = ['Binnen5Km_12', 'Codering_3', 'Binnen3Km_7', 'Binnen5Km_12', 'Binnen10Km_13',
                     'Binnen5Km_16', 'Binnen10Km_17', 'regio', 'Binnen1Km_6']


column_mapping = {
                'PC4': 'pc4_code',
                'AfstandTotHuisartsenpraktijk_5': 'afstand_tot_huisartsenpraktijk',
                'Binnen5Km_8': 'hpa_binnen_5km',
                'AfstandTotZiekenhuis_11': 'afstand_tot_ziekenhuis_excl',
                'Binnen20Km_14': 'ze_binnen_20km',
                'AfstandTotZiekenhuis_15': 'afstand_tot_ziekenhuis_incl',
                'Binnen20Km_18': 'zi_binnen_20km',
                'AfstandTotHuisartsenpost_9': 'afstand_tot_huisartsenpost',

                  }
# new_column_name = 'jaartal'
# new_column_value = 2022
# output_filename = 'hittestress_2022.xlsx'


df = pd.read_excel(file_path)
# df = excel_scripts.add_column(df, new_column_name, new_column_value)
df = excel_scripts.remove_columns(df, columns_to_remove)
df = excel_scripts.rename_columns(df, column_mapping)
excel_scripts.turn_df_into_excel(df, output_filename)