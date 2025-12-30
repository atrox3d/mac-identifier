from pathlib import Path
import pytest
from dotenv import load_dotenv, dotenv_values

ENV = dotenv_values()
print('CONFTEST.PY', ENV)
SECRET_DIR            = ENV.get('SECRET_DIR')

EMPTY_FILENAME        = ENV.get('EMPTY_FILENAME')

ROUTER_DHCP_FILENAME  = ENV.get('ROUTER_DHCP_FILENAME')
ROUTER_DHCP_COLUMNS   = ENV.get('ROUTER_DHCP_COLUMNS')

KNOWN_MACS_FILENAME   = ENV.get('KNOWN_MACS_FILENAME')
KNOWN_MACS_COLUMNS    = ENV.get('KNOWN_MACS_COLUMNS')

UNKNOWN_MACS_FILENAME = ENV.get('UNKNOWN_MACS_FILENAME')
UNKNOWN_MACS_COLUMNS  = ENV.get('UNKNOWN_MACS_COLUMNS')


@pytest.fixture
def secret_dir() -> Path:
    path = Path(SECRET_DIR).resolve()
    # print(path)
    return path


@pytest.fixture
def empty_txt_path(secret_dir: Path) -> Path:
    path = secret_dir / EMPTY_FILENAME
    # print(path)
    return path


@pytest.fixture
def router_txt_path(secret_dir: Path) -> Path:
    path = secret_dir / ROUTER_DHCP_FILENAME
    # print(path)
    return path


@pytest.fixture
def router_txt_columns() -> list[str]:
    return [name.strip() for name in ROUTER_DHCP_COLUMNS.split(',')]


@pytest.fixture
def known_macs_txt_path(secret_dir: Path) -> Path:
    path = secret_dir / KNOWN_MACS_FILENAME
    # print(path)
    return path


@pytest.fixture
def known_macs_columns() -> list[str]:
    return [name.strip() for name in KNOWN_MACS_COLUMNS.split(',')]


@pytest.fixture
def unknown_macs_columns() -> list[str]:
    return [name.strip() for name in UNKNOWN_MACS_COLUMNS.split(',')]


@pytest.fixture
def unknown_macs_txt_path(secret_dir: Path) -> Path:
    path = secret_dir / UNKNOWN_MACS_FILENAME
    # print(path)
    return path