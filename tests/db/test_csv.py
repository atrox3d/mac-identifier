import pytest
from pathlib import Path
import pandas as pd

from db import csv


def test_load_empty_csv_fails(empty_txt_path: Path):
    with pytest.raises(pd.errors.EmptyDataError):
        df = csv.load_csv(empty_txt_path)


def test_load_router_csv(router_txt_path: Path, router_txt_columns: list[str]):
    df = csv.load_csv(router_txt_path)
    print(df.columns)
    print(df)
    print(df.shape)
    assert df.shape == (11, 3)
    assert list(df.columns) == router_txt_columns


def test_get_router_dhcp_table(router_txt_path: Path):
    df = csv.load_csv(router_txt_path)
    df = csv.get_mac_ref_table(df, descr_col=1, mac_col=0, sep=':', replace='-')
    print(df.columns)
    print(df)
    # Explicitly filter for True values and then count them
    matches = df.iloc[:, 0].str.contains(':')
    print(matches[matches == True].count())
    assert matches[matches == True].count() == 0


def test_load_known_macs(known_macs_txt_path: Path, known_macs_columns: list[str]):
    df = csv.load_csv(known_macs_txt_path, separator=';')
    print(df.columns)
    print(df)
    print(df.shape)
    assert df.shape == (14, 2)
    assert list(df.columns) == known_macs_columns


def test_get_known_macs_table(known_macs_txt_path: Path):
    df = csv.load_csv(known_macs_txt_path, separator=';')
    df = csv.get_mac_ref_table(df, descr_col=1, mac_col=0, sep='-', replace=':')
    print(df.columns)
    print(df)
    matches = df.iloc[:, 0].str.contains('-')
    print(matches[matches == True].count())
    assert matches[matches == True].count() == 0


def test_load_unknown_macs(unknown_macs_txt_path: Path, unknown_macs_columns: list[str]):
    df = csv.load_csv(unknown_macs_txt_path, separator=';')
    print(df.columns)
    print(df)
    print(df.shape)
    assert df.shape == (11, 2)
    assert list(df.columns) == unknown_macs_columns


def test_get_unknown_macs_table(unknown_macs_txt_path: Path):
    df = csv.load_csv(unknown_macs_txt_path, separator=';')
    df = csv.get_mac_ref_table(df, descr_col=1, mac_col=0, sep='-', replace=':')
    print(df.columns)
    print(df)
    matches = df.iloc[:, 0].str.contains('-')
    print(matches[matches == True].count())
    assert matches[matches == True].count() == 0
