from pathlib import Path
import pytest
import pandas as pd

from db import csv


SECRET_DIR = 'secret'
ROUTER_TXT = 'router-dhcp.txt'


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


def test_load_txt_csv(router_txt_path):
    df = csv.load_txt_csv(router_txt_path, separator='\t')
    print(df.columns)
    print(df)
    print(df.count())


def test_get_dhcp_table(router_txt_path):
    df = csv.load_txt_csv(router_txt_path, separator='\t')
    df = csv.get_dhcp_table(df, 1, 2, ':', '-')
    print(df.columns)
    print(df)
    