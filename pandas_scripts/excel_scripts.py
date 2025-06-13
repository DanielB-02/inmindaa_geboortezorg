import pandas as pd


def remove_columns(dataframe, columns_to_remove):
    """
    Remove specified columns from the dataframe.
    """
    return dataframe.drop(columns=columns_to_remove, errors='ignore')


def rename_columns(dataframe, column_mapping):
    """
    Rename columns in the dataframe based on a mapping.
    """
    return dataframe.rename(columns=column_mapping)


def add_column(dataframe, column_name, default_value):
    """
    Add a new column to the DataFrame with a default value.
    """
    dataframe[column_name] = default_value
    return dataframe


def turn_df_into_excel(df, file_name):
    """
    Save the DataFrame to an Excel file in the 'bewerkte_data' folder.
    """
    df.to_excel(f"../bewerkte_data/{file_name}", index=False)
