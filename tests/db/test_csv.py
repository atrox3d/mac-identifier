from pathlib import Path
import pandas as pd

from db import csv


def test_load_txt_csv(router_txt_path: Path):
    df = csv.load_txt_csv(router_txt_path)
    print(df.columns)
    print(df)
    print(df.shape)
    assert df.shape == (11, 3)
    assert list(df.columns) == ['IPv4', 'MAC', 'Dispositivo']


def test_get_dhcp_table(router_txt_path: Path):
    df = csv.load_txt_csv(router_txt_path)
    df = csv.get_mac_ref_table(df, descr_col=1, mac_col=0, sep=':', replace='-')
    print(df.columns)
    print(df)
    # Explicitly filter for True values and then count them
    matches = df.iloc[:, 0].str.contains(':')
    print(matches[matches == True].count())
    assert matches[matches == True].count() == 0


def test_load_mymacs(known_macs_txt_path: Path):
    df = csv.load_txt_csv(known_macs_txt_path, separator=';')
    print(df.columns)
    print(df)
    print(df.shape)
    assert df.shape == (14, 2)
    assert list(df.columns) == ['mac', 'description']


def test_get_mymacs_table(known_macs_txt_path: Path):
    df = csv.load_txt_csv(known_macs_txt_path, separator=';')
    df = csv.get_mac_ref_table(df, descr_col=1, mac_col=0, sep='-', replace=':')
    print(df.columns)
    print(df)
    matches = df.iloc[:, 0].str.contains('-')
    print(matches[matches == True].count())
    assert matches[matches == True].count() == 0


def test_load_hismacs(unknown_macs_txt_path: Path):
    df = csv.load_txt_csv(unknown_macs_txt_path, separator=';')
    print(df.columns)
    print(df)
    print(df.shape)
    assert df.shape == (11, 2)
    assert list(df.columns) == ['mac', 'description']


def test_get_hismacs_table(unknown_macs_txt_path: Path):
    df = csv.load_txt_csv(unknown_macs_txt_path, separator=';')
    df = csv.get_mac_ref_table(df, descr_col=1, mac_col=0, sep='-', replace=':')
    print(df.columns)
    print(df)
    matches = df.iloc[:, 0].str.contains('-')
    print(matches[matches == True].count())
    assert matches[matches == True].count() == 0
