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


def drop_duplicate_rows(dataframe, columns):
    """
    Drop duplicate rows, uses the given list of columns to determine if there are duplicate rows.
    """
    return dataframe.drop_duplicates(subset=columns, inplace=True)


def delete_rows_on_substrings_excel(file_path, column_name, substrings_to_delete):
    """
        Example of implementation:
            file_path = 'old_zorgaanbod_2022.xlsx'
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


def merge_excel_files(main_excel_file, second_excel_file, merged_excel_file, main_merge_column, second_merge_column):
    """
    Left merge two Excel files on the two given columns
    These columns need to have the same kind of data, for example PC4 codes
    """
    df_main = pd.read_excel(main_excel_file, dtype=str)
    df2 = pd.read_excel(second_excel_file, dtype=str)

    df_main[main_merge_column] = df_main[main_merge_column].astype(str).str.strip()
    df2[second_merge_column] = df2[second_merge_column].astype(str).str.strip()

    df_merged = pd.merge(df_main, df2, left_on=main_merge_column, right_on=second_merge_column, how='left')

    df_merged.to_excel(merged_excel_file, index=False)


def add_pc4_to_excel(dataset, locatie_dataset, locatie_code_column, locatie_dataset_code_column, file_name):
    """
    Add PC4 codes to an Excel file
    This will create new rows based on the combination of the location and PC4 codes
    """
    df = pd.read_excel(dataset)

    ld_frame = pd.read_excel(locatie_dataset)
    ld_frame = ld_frame[[locatie_dataset_code_column, "PC4"]]

    df = pd.merge(df, ld_frame, left_on=[locatie_code_column], right_on=[locatie_dataset_code_column],
                         how='left')

    df.drop(columns=[locatie_dataset_code_column], inplace=True)
    df = df.drop_duplicates()
    df.to_excel(f"../bewerkte_data/{file_name}", index=False)

    return df