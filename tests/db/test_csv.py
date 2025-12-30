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
    df = csv.build_mac_ref_table(df, descr_col=0, mac_col=1, sep=':', replace=':', name_col_name='ip')
    print(df.columns)
    print(df)
    # Explicitly filter for True values and then count them
    matches = df.iloc[:, 0].str.contains('-')
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
    df = csv.build_mac_ref_table(df, descr_col=1, mac_col=0, sep='-', replace=':')
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
    df = csv.build_mac_ref_table(df, descr_col=1, mac_col=0, sep='-', replace=':')
    print(df.columns)
    print(df)
    matches = df.iloc[:, 0].str.contains('-')
    print(matches[matches == True].count())
    assert matches[matches == True].count() == 0


def test_stack_mac_ref_tables(known_macs_txt_path: Path, unknown_macs_txt_path: Path):
    known_macs_df = csv.load_csv(known_macs_txt_path, separator=';')
    unknown_macs_df = csv.load_csv(unknown_macs_txt_path, separator=';')
    stacked = csv.stack_mac_ref_tables(known_macs_df, unknown_macs_df)
    print(stacked.columns)
    print(stacked)
    print(stacked.shape)
    assert stacked.shape == (known_macs_df.shape[0] + unknown_macs_df.shape[0], 2)


def test_merge(router_txt_path, known_macs_txt_path: Path, unknown_macs_txt_path: Path):
    router_dhcp_df = csv.load_csv(router_txt_path)
    router_dhcp_df = csv.build_mac_ref_table(router_dhcp_df, descr_col=0, mac_col=1, sep=':', replace=':', name_col_name='ip')
    print(router_dhcp_df.columns)

    known_macs_df = csv.load_csv(known_macs_txt_path, separator=';')
    known_macs_df = csv.build_mac_ref_table(known_macs_df, descr_col=1, mac_col=0, sep='-', replace=':')
    print(known_macs_df.columns)

    unknown_macs_df = csv.load_csv(unknown_macs_txt_path, separator=';')
    unknown_macs_df = csv.build_mac_ref_table(unknown_macs_df, descr_col=1, mac_col=0, sep='-', replace=':')
    print(unknown_macs_df.columns)
    
    stacked = csv.stack_mac_ref_tables(known_macs_df, unknown_macs_df)
    print(unknown_macs_df.columns)

    merged = csv.merge_and_fill(
        router_dhcp_df, 
        stacked, 
        on='mac', fill_col='name')
    print(merged.columns)
    print(merged)
    assert len(merged) == len(router_dhcp_df)

    total_unknowns = len(merged[merged['name']=='UNKNOWN'])
    assert total_unknowns == 2
    
    distinct = merged[['mac', 'name']].drop_duplicates()
    print(distinct)
    assert len(distinct) == 10
