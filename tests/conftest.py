from pathlib import Path
import pytest
from dotenv import load_dotenv, dotenv_values

# print('CONFTEST.PY', Path.cwd())
ENV = dotenv_values()
SECRET_DIR            = ENV.get('SECRET_DIR')
ROUTER_TXT_FILENAME   = ENV.get('ROUTER_TXT_FILENAME')
KNOWN_MACS_FILENAME   = ENV.get('KNOWN_MACS_FILENAME')
UNKNOWN_MACS_FILENAME = ENV.get('UNKNOWN_MACS_FILENAME')


@pytest.fixture
def secret_dir() -> Path:
    path = Path(SECRET_DIR).resolve()
    # print(path)
    return path


@pytest.fixture
def router_txt_path(secret_dir: Path) -> Path:
    path = secret_dir / ROUTER_TXT_FILENAME
    # print(path)
    return path


@pytest.fixture
def known_macs_txt_path(secret_dir: Path) -> Path:
    path = secret_dir / KNOWN_MACS_FILENAME
    # print(path)
    return path


@pytest.fixture
def unknown_macs_txt_path(secret_dir: Path) -> Path:
    path = secret_dir / UNKNOWN_MACS_FILENAME
    # print(path)
    return path