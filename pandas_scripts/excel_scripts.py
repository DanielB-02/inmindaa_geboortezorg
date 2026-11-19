"""Reusable pandas helpers for cleaning the raw datasets before loading them into PostgreSQL."""

from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
PROCESSED_DIR = ROOT_DIR / "bewerkte_data"


def remove_columns(dataframe: pd.DataFrame, columns_to_remove: list[str]) -> pd.DataFrame:
    """
    Remove specified columns from the dataframe.
    """
    return dataframe.drop(columns=columns_to_remove, errors="ignore")


def rename_columns(dataframe: pd.DataFrame, column_mapping: dict[str, str]) -> pd.DataFrame:
    """
    Rename columns in the dataframe based on a mapping.
    """
    return dataframe.rename(columns=column_mapping)


def add_column(dataframe: pd.DataFrame, column_name: str, default_value) -> pd.DataFrame:
    """
    Add a new column to the DataFrame with a default value.
    Note: the DataFrame is modified in place and also returned.
    """
    dataframe[column_name] = default_value
    return dataframe


def turn_df_into_excel(df: pd.DataFrame, file_name: str) -> None:
    """
    Save the DataFrame to an Excel file in the 'bewerkte_data' folder.
    """
    df.to_excel(PROCESSED_DIR / file_name, index=False)


def drop_duplicate_rows(dataframe: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Drop duplicate rows, uses the given list of columns to determine if there are duplicate rows.
    """
    return dataframe.drop_duplicates(subset=columns, keep="first")


def drop_rows_from_column_with_null_values(dataframe: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Drop rows from the DataFrame where the specified column has null values.
    """
    return dataframe.dropna(subset=[column_name])


def delete_rows_on_substrings_excel(
    dataframe: pd.DataFrame, column_name: str, substrings_to_delete: list[str]
) -> pd.DataFrame:
    """
    Delete every row whose value in `column_name` contains one of the substrings (case-insensitive).

    Example:
        df = pd.read_excel(DATA_DIR / "copy_zorgaanbod_2022.xlsx")
        df = delete_rows_on_substrings_excel(df, "Codering_3", ["WK", "BU", "NL"])
    """
    rows_to_delete = pd.Series([False] * len(dataframe), index=dataframe.index)
    for sub in substrings_to_delete:
        rows_with_substring = dataframe[column_name].astype(str).str.contains(sub, na=False, case=False)
        rows_to_delete = rows_to_delete | rows_with_substring
    df_updated = dataframe[~rows_to_delete]
    return df_updated


def merge_excel_files(
    main_excel_file, second_excel_file, merged_excel_file, main_merge_column: str, second_merge_column: str
) -> None:
    """
    Left merge two Excel files on the two given columns
    These columns need to have the same kind of data, for example PC4 codes
    """
    df_main = pd.read_excel(main_excel_file, dtype=str)
    df2 = pd.read_excel(second_excel_file, dtype=str)

    df_main[main_merge_column] = df_main[main_merge_column].astype(str).str.strip()
    df2[second_merge_column] = df2[second_merge_column].astype(str).str.strip()

    df_merged = pd.merge(df_main, df2, left_on=main_merge_column, right_on=second_merge_column, how="left")

    df_merged.to_excel(merged_excel_file, index=False)


def add_pc4_to_dataframe(
    dataframe: pd.DataFrame, locatie_dataset, locatie_code_column: str, locatie_dataset_code_column: str
) -> pd.DataFrame:
    """
    Add PC4 codes to a dataframe
    This will create new rows based on the combination of the location and PC4 codes
    """

    ld_frame = pd.read_excel(locatie_dataset)
    ld_frame = ld_frame[[locatie_dataset_code_column, "PC4"]]

    df = pd.merge(
        dataframe, ld_frame, left_on=[locatie_code_column], right_on=[locatie_dataset_code_column], how="left"
    )

    df.drop(columns=[locatie_dataset_code_column], inplace=True)
    df = df.drop_duplicates()

    return df
