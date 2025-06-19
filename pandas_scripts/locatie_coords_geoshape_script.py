import pandas as pd
import pandas_scripts.excel_scripts as exs
import geopandas as gpd
from shapely.geometry import shape
import json

def get_and_prepare_dataframes():
    df_locatie = pd.read_excel("../bewerkte_data/locatie.xlsx")
    df_coords = pd.read_csv("../data/georef-netherlands-postcode-pc4.csv", sep=';')
    df_locatie['pc4_code'] = df_locatie['pc4_code'].astype(str).str.strip()
    df_coords['PC4'] = df_coords['PC4'].astype(str).str.strip()
    return df_locatie, df_coords


def merge_locatie_and_coords_on_pc4(df_left, df_right):
    df_merged = pd.merge(df_left, df_right, left_on='pc4_code', right_on='PC4', how='left')
    df_merged = exs.remove_columns(df_merged, ['PC4'])
    return df_merged


def split_geo_point(df):
    df[['latitude', 'longitude']] = df['Geo Point'].str.split(',', expand=True)
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].str.strip().astype(float)
    df = exs.remove_columns(df, ['Geo Point'])
    return df


def create_locatie_coords(excel_file_name):
    df_locatie, df_coords = get_and_prepare_dataframes()
    df_coords = df_coords[['PC4', 'Geo Point']]

    # De pc4_codes waarvan de coördinaten misten
    missing_coords = {
        '2236': '52.17271, 4.41495',
        '8269': '52.5285, 5.88114',
        '8323': '52.6537999, 5.6396',
        '1364': '52.3837, 5.12875'
        }

    # Voegt de dataframes samen en verwijderd daarna de extra PC4 kolom
    df_merged = merge_locatie_and_coords_on_pc4(df_locatie, df_coords)

    # Voegt de missende coördinaten toe aan de juiste pc4 codes
    for pc4_code, GeoPoint in missing_coords.items():
        df_merged.loc[df_locatie['pc4_code'] == pc4_code, ['Geo Point']] = GeoPoint

    # Splits de coördinaten op en slaat ze op in de kolommen latitude en longitude, verwijderd daarna Geo Point.
    df_merged = split_geo_point(df_merged)

    print(df_merged.head())
    print(df_merged.nunique())

    exs.turn_df_into_excel(df_merged, excel_file_name)


def create_locatie_geoshape(csv_file_name):
    df_locatie, df_coords = get_and_prepare_dataframes()

    df_coords = df_coords[['PC4', 'Geo Point', 'Geo Shape']]

    # Verwijder de pc4_codes waarvoor geen Geo Shape voor is
    te_verwijderen_pc4 = ['2236', '8269', '8323', '1364']
    df_locatie = df_locatie[~df_locatie['pc4_code'].isin(te_verwijderen_pc4)]

    # Voegt de dataframes samen en verwijderd daarna de extra PC4 kolom
    df_merged = merge_locatie_and_coords_on_pc4(df_locatie, df_coords)

    # Splits de coördinaten op en slaat ze op in de kolommen latitude en longitude, verwijderd daarna Geo Point.
    df_merged = split_geo_point(df_merged)

    df_merged["Geo Shape"] = df_merged["Geo Shape"].apply(lambda x: json.loads(x) if isinstance(x, str) else x)

    # Checken op Nan Values
    invalid = df_merged[~df_merged["Geo Shape"].apply(lambda x: isinstance(x, dict))]
    print(invalid[["pc4_code", "Geo Shape"]])

    df_merged["Geo Shape"] = df_merged["Geo Shape"].apply(json.dumps)
    df_merged.to_csv(f"../bewerkte_data/{csv_file_name}", index=False)


def get_geodataframe():
    df_geoshape = pd.read_csv("../bewerkte_data/locatie_geoshape.csv", sep=',')

    # Laad Geo Shape terug in als dict
    df_geoshape["Geo Shape"] = df_geoshape["Geo Shape"].apply(json.loads)

    # Checken op Nan Values
    invalid = df_geoshape[~df_geoshape["Geo Shape"].apply(lambda x: isinstance(x, dict))]
    print(invalid[["pc4_code", "Geo Shape"]])

    # Zet een Python dictionary (in GeoJSON-formaat) om naar een echte Shapely-geometry zoals een Polygon of MultiPolygon
    df_geoshape["geometry"] = df_geoshape["Geo Shape"].apply(shape)

    # Zet de dataframe om naar een Geodataframe
    gdf = gpd.GeoDataFrame(df_geoshape, geometry="geometry")
    gdf.set_crs(epsg=4326, inplace=True)

    gdf.head()
    return gdf