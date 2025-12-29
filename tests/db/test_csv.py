from pathlib import Path
import pytest
import pandas as pd

from db import csv


SECRET_DIR = 'secret'
ROUTER_TXT = 'router-dhcp.txt'
MY_MACS = 'my-macs.txt'
HIS_MACS = 'his-macs.txt'



@pytest.fixture
def secret_dir() -> Path:
    path = Path(SECRET_DIR).resolve()
    # print(path)
    return path


@pytest.fixture
def router_txt_path(secret_dir: Path) -> Path:
    path = secret_dir / ROUTER_TXT
    # print(path)
    return path


@pytest.fixture
def mymacs_txt_path(secret_dir: Path) -> Path:
    path = secret_dir / MY_MACS
    # print(path)
    return path


@pytest.fixture
def hismacs_txt_path(secret_dir: Path) -> Path:
    path = secret_dir / HIS_MACS
    # print(path)
    return path


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


def test_load_mymacs(mymacs_txt_path: Path):
    df = csv.load_txt_csv(mymacs_txt_path, separator=';')
    print(df.columns)
    print(df)
    print(df.shape)
    assert df.shape == (14, 2)
    assert list(df.columns) == ['mac', 'description']


def test_get_mymacs_table(mymacs_txt_path: Path):
    df = csv.load_txt_csv(mymacs_txt_path, separator=';')
    df = csv.get_mac_ref_table(df, descr_col=1, mac_col=0, sep='-', replace=':')
    print(df.columns)
    print(df)
    matches = df.iloc[:, 0].str.contains('-')
    print(matches[matches == True].count())
    assert matches[matches == True].count() == 0


def test_load_hismacs(hismacs_txt_path: Path):
    df = csv.load_txt_csv(hismacs_txt_path, separator=';')
    print(df.columns)
    print(df)
    print(df.shape)
    assert df.shape == (11, 2)
    assert list(df.columns) == ['mac', 'description']


def test_get_hismacs_table(hismacs_txt_path: Path):
    df = csv.load_txt_csv(hismacs_txt_path, separator=';')
    df = csv.get_mac_ref_table(df, descr_col=1, mac_col=0, sep='-', replace=':')
    print(df.columns)
    print(df)
    matches = df.iloc[:, 0].str.contains('-')
    print(matches[matches == True].count())
    assert matches[matches == True].count() == 0
