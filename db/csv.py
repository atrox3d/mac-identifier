from pathlib import Path
import pandas as pd

# Matches tabs OR 2+ whitespace characters.
# This allows descriptions to contain single spaces (e.g., "tv LG") without breaking the row.
# SEP_REGEX = r'\t+|\s+'
SEP_REGEX = r'\s+'
INFER_HEADER = 0


def load_txt_csv(
        filepath:str | Path, 
        header=INFER_HEADER,
        separator:str=SEP_REGEX,
        names=None,
        comment:str='#',
        **kwargs
) -> pd.DataFrame:
    df = pd.read_csv(
        filepath,
        sep=separator,
        header=header,
        names=names,
        comment=comment,
        **kwargs
    )
    return df


def get_mac_ref_table(
    df:pd.DataFrame,
    # ip_column:int|str,
    descr_col:int|str,
    mac_col:int|str,
    sep:str,
    replace:str=':'
) -> pd.DataFrame:
    """
    Extracts and cleans IP and MAC columns from a DataFrame.
    
    Args:
        ip_column: Name (str) or index (int) of the IP column.
        mac_column: Name (str) or index (int) of the MAC column.
    """
    # mac_col = df.columns[mac_column] if isinstance(mac_column, int) else mac_column
    cols = [
        df.columns[col] if isinstance(col, int) else col
        for col in [descr_col, mac_col]
    ]
    descr, mac = cols
    df[mac] = df[mac].str.replace(
        sep,
        replace,
        regex=False
    )
    df = df[[mac, descr]]
    df.columns = ['mac', 'name']
    return df
