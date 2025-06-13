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


def delete_rows_on_substrings_excel(file_path, column_name, substrings_to_delete):
    """
        Example of implementation:
            file_path = 'zorgaanbod_2022.xlsx'
            column_name = 'Codering_3'
            substrings_to_delete = ['WK', 'BU']
        delete_rows_on_substrings_excel(file_path, column_name, substrings_to_delete)
    """
    df = pd.read_excel(file_path)
    rows_to_delete = pd.Series([False] * len(df), index=df.index)
    for sub in substrings_to_delete:
        rows_with_substring = df[column_name].astype(str).str.contains(sub, na=False, case=False)
        rows_to_delete = rows_to_delete | rows_with_substring
    df_updated = df[~rows_to_delete]
    df_updated.to_excel(file_path, index=False)
    return True