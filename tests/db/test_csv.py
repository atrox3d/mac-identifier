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
def router_txt_path(secret_dir) -> Path:
    path = secret_dir / ROUTER_TXT
    # print(path)
    return path


@pytest.fixture
def mymacs_txt_path(secret_dir) -> Path:
    path = secret_dir / MY_MACS
    # print(path)
    return path


@pytest.fixture
def hismacs_txt_path(secret_dir) -> Path:
    path = secret_dir / HIS_MACS
    # print(path)
    return path


def test_load_txt_csv(router_txt_path):
    df = csv.load_txt_csv(router_txt_path)
    print(df.columns)
    print(df)
    print(df.count())


def test_get_dhcp_table(router_txt_path):
    df = csv.load_txt_csv(router_txt_path)
    df = csv.get_dhcp_table(df, 1, 2, ':', '-')
    print(df.columns)
    print(df)


def test_load_mymacs(mymacs_txt_path):
    df = csv.load_txt_csv(mymacs_txt_path, separator=';')
    print(df.columns)
    print(df)


def test_get_mymacs_table(mymacs_txt_path):
    df = csv.load_txt_csv(mymacs_txt_path, separator=';')
    df = csv.get_dhcp_table(df, 0, '-', ':')
    print(df.columns)
    print(df)


def test_load_hismacs(hismacs_txt_path):
    df = csv.load_txt_csv(hismacs_txt_path, separator=';')
    print(df.columns)
    print(df)


def test_get_hismacs_table(hismacs_txt_path):
    df = csv.load_txt_csv(hismacs_txt_path, separator=';')
    df = csv.get_dhcp_table(df, 0, '-', ':')
    print(df.columns)
    print(df)