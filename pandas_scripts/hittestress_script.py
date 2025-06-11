import pandas as pd

file_path = '../data/gevoelstemperatuurPC4_2022.xlsx'
df = pd.read_excel(file_path)


def remove_columns(dataframe, columns_to_remove):
    """
    Remove specified columns from the dataframe.

    :param dataframe: The pandas DataFrame from which to remove columns.
    :param columns_to_remove: List of column names to be removed.
    :return: DataFrame with specified columns removed.
    """
    return dataframe.drop(columns=columns_to_remove, errors='ignore')


def rename_columns(dataframe, column_mapping):
    """
    Rename columns in the dataframe based on a mapping.

    :param dataframe: The pandas DataFrame whose columns are to be renamed.
    :param column_mapping: Dictionary mapping old column names to new names.
    :return: DataFrame with renamed columns.
    """
    return dataframe.rename(columns=column_mapping)


def add_column(dataframe, column_name, default_value):
    """
    Add a new column to the DataFrame with a default value.

    :param dataframe: The pandas DataFrame to which the column will be added.
    :param column_name: The name of the new column.
    :param default_value: The default value for the new column.
    :return: DataFrame with the new column added.
    """
    dataframe[column_name] = default_value
    return dataframe


def turn_df_into_excel(df, file_name):
    """
    Save the DataFrame to an Excel file in the 'bewerkte_data' folder.

    :param df: The pandas DataFrame to save.
    :param file_name: The name of the output Excel file.
    """

    df.to_excel(f"../bewerkte_data/{file_name}", index=False)


removed_columns_df = remove_columns(df,
                                    ['fid', 'fid_1', 'buurtcode', 'buurtnaam', 'wijkcode',
                                     'gemeenteco', 'gemeentena', 'jrstatcode', 'jaar'])

renamed_columns_df = rename_columns(removed_columns_df, {'PC4': 'pc4_code'})

add_columns_df = add_column(renamed_columns_df, 'jaartal', 2022)

turn_df_into_excel(add_columns_df, 'hittestress_2022.xlsx')
