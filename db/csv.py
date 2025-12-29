from pathlib import Path
import pandas as pd

TAB = '\t'
SPACES = 's+'
SEP_REGEX = f'{TAB}|{SPACES}'
INFER_HEADER = 0


def load_txt_csv(
        filepath:str, 
        header=INFER_HEADER,
        separator:str=SEP_REGEX,
        names=None
) -> pd.DataFrame:
    df = pd.read_csv(
        filepath,
        sep=separator,
        header=header,
        names=names
    )
    return df


def get_dhcp_table(
    df:pd.DataFrame,
    ip_column:int|str,
    mac_column:int|str,
    mac_sep:str,
    mac_replace_sep:str=':'
) -> pd.DataFrame:
    # df = df.loc[[ip_column, mac_column]:]
    columns = [
        df.columns[i] if isinstance(i, int) else i
        for i in [ip_column, mac_column]
    ]
    df = df[columns]
    ip_col, mac_col = columns
    df[mac_col] = df[mac_col].str.replace(
        mac_sep,
        mac_replace_sep
    )
    return df

