import pandas as pd
import pandas_scripts.excel_scripts as exs

df = pd.read_excel("../bewerkte_data/locatie.xlsx")
df_coords = pd.read_excel("../data/georef-netherlands-postcode-pc4.xlsx")

df['pc4_code'] = df['pc4_code'].astype(str).str.strip()
df_coords['PC4'] = df_coords['PC4'].astype(str).str.strip()

df_coords = df_coords[['PC4', 'Geo Point']]

# De pc4_codes waarvan de coördinaten misten
MissingCoords = {
    '2236': '52.17271, 4.41495',
    '8269': '52.5285, 5.88114',
    '8323': '52.6537999, 5.6396',
    '1364': '52.3837, 5.12875'
    }

# Voegt de dataframes samen en verwijderd daarna de extra PC4 kolom
df_merged = pd.merge(df, df_coords, left_on='pc4_code', right_on='PC4', how='left')
df_merged = exs.remove_columns(df_merged, ['PC4'])

# Voegt de missende coördinaten toe aan de juiste pc4 codes
for pc4_code, GeoPoint in MissingCoords.items():
    df_merged.loc[df['pc4_code'] == pc4_code, ['Geo Point']] = GeoPoint

# Splits de coördinaten in Geo Point op en slaat ze op in de kolommen latitude en longitude
df_merged[['latitude', 'longitude']] = df_merged['Geo Point'].str.split(',', expand=True)
df_merged['latitude'] = df_merged['latitude'].astype(float)
df_merged['longitude'] = df_merged['longitude'].str.strip().astype(float)

df_merged = exs.remove_columns(df_merged, ['Geo Point'])

print(df_merged.head())
print(df_merged.nunique())

exs.turn_df_into_excel(df_merged, 'locatie_coords.xlsx')