from pathlib import Path
import pytest

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