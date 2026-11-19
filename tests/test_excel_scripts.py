import pandas as pd
import pytest

from pandas_scripts import excel_scripts as exs


@pytest.fixture
def regions() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "code": ["GM0363", "WK036300", "BU03630000", "NL00", "GM0599"],
            "value": [1, 2, 3, 4, 5],
        }
    )


def test_delete_rows_on_substrings_keeps_only_municipalities(regions):
    result = exs.delete_rows_on_substrings_excel(regions, "code", ["WK", "BU", "NL"])
    assert result["code"].tolist() == ["GM0363", "GM0599"]


def test_delete_rows_on_substrings_is_case_insensitive_and_handles_non_strings():
    df = pd.DataFrame({"jaar": [2020, 2022, None], "x": [1, 2, 3]})
    result = exs.delete_rows_on_substrings_excel(df, "jaar", ["2020"])
    assert result["x"].tolist() == [2, 3]

    df = pd.DataFrame({"code": ["wk01", "GM01"]})
    assert exs.delete_rows_on_substrings_excel(df, "code", ["WK"])["code"].tolist() == ["GM01"]


def test_remove_columns_ignores_missing_columns(regions):
    result = exs.remove_columns(regions, ["value", "does_not_exist"])
    assert list(result.columns) == ["code"]


def test_rename_columns(regions):
    result = exs.rename_columns(regions, {"code": "gwb_code"})
    assert list(result.columns) == ["gwb_code", "value"]


def test_add_column_sets_constant_value(regions):
    result = exs.add_column(regions, "jaartal", 2022)
    assert (result["jaartal"] == 2022).all()


def test_drop_duplicate_rows_uses_subset_and_keeps_first():
    df = pd.DataFrame({"PC4": [1000, 1000, 2000], "lbm": [3.9, 4.1, 4.0]})
    result = exs.drop_duplicate_rows(df, ["PC4"])
    assert result["lbm"].tolist() == [3.9, 4.0]


def test_drop_rows_from_column_with_null_values():
    df = pd.DataFrame({"a": [1.0, None, 3.0], "b": [None, 2, 3]})
    result = exs.drop_rows_from_column_with_null_values(df, "a")
    assert result["a"].tolist() == [1.0, 3.0]


def test_add_pc4_to_dataframe_expands_rows_per_postcode(tmp_path):
    locations = pd.DataFrame(
        {
            "GemCode": ["GM0363", "GM0363", "GM0363", "GM0599"],
            "PC4": [1011, 1012, 1012, 3011],  # duplicate GM0363/1012 (e.g. multiple PC6s)
        }
    )
    location_file = tmp_path / "locaties.xlsx"
    locations.to_excel(location_file, index=False)

    df = pd.DataFrame({"code": ["GM0363", "GM0599", "GM9999"], "value": [10, 20, 30]})
    result = exs.add_pc4_to_dataframe(df, location_file, "code", "GemCode")

    assert "GemCode" not in result.columns
    assert result.sort_values("PC4", na_position="last")[["code", "PC4"]].values.tolist()[:3] == [
        ["GM0363", 1011],
        ["GM0363", 1012],
        ["GM0599", 3011],
    ]
    assert len(result) == 4  # unknown municipality kept with missing PC4 (left join)
    assert result.loc[result["code"] == "GM9999", "PC4"].isna().all()


def test_turn_df_into_excel_writes_to_processed_dir(tmp_path, monkeypatch, regions):
    monkeypatch.setattr(exs, "PROCESSED_DIR", tmp_path)
    exs.turn_df_into_excel(regions, "out.xlsx")
    pd.testing.assert_frame_equal(pd.read_excel(tmp_path / "out.xlsx"), regions)


def test_merge_excel_files_left_joins_on_stripped_strings(tmp_path):
    main, other, out = tmp_path / "main.xlsx", tmp_path / "other.xlsx", tmp_path / "out.xlsx"
    pd.DataFrame({"pc4_code": ["1011 ", "2000"], "a": [1, 2]}).to_excel(main, index=False)
    pd.DataFrame({"PC4": [" 1011"], "b": ["x"]}).to_excel(other, index=False)

    exs.merge_excel_files(main, other, out, "pc4_code", "PC4")

    result = pd.read_excel(out, dtype=str)
    assert result["pc4_code"].tolist() == ["1011", "2000"]
    assert result["b"].tolist()[0] == "x"
    assert pd.isna(result["b"].tolist()[1])
