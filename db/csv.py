from pathlib import Path
import pandas as pd

SEP_REGEX = r'\s+'
INFER_HEADER = 0


def load_csv(
        filepath:str | Path, 
        header=INFER_HEADER,
        separator:str=SEP_REGEX,
        # names=None,
        comment:str='#',
        **kwargs
) -> pd.DataFrame:
    '''
    raises: pandas.errors.EmptyDataError if file is empty
    '''
    df = pd.read_csv(
        filepath,
        sep=separator,
        header=header,
        # names=names,
        comment=comment,
        **kwargs
    )
    return df


def build_mac_ref_table(
    df:pd.DataFrame,
    descr_col:int|str,
    mac_col:int|str,
    sep:str,
    replace:str,
    mac_col_name:str='mac',
    name_col_name:str='name'
) -> pd.DataFrame:
    
    # get column names as str from int idx or name
    cols = [
        df.columns[col] if isinstance(col, int) else col
        for col in [descr_col, mac_col]
    ]
    descr, mac = cols
    
    # fix mac format
    df[mac] = df[mac].str.replace(
        sep,
        replace,
        regex=False
    )

    # extract only relevant columns
    df = df[[mac, descr]]
    # rename columns
    df.columns = [mac_col_name, name_col_name]
    return df


def stack_mac_ref_tables(*dfs:pd.DataFrame) -> pd.DataFrame:
    return pd.concat(dfs, ignore_index=True)


def merge_and_fill(
    left_df: pd.DataFrame,
    right_df: pd.DataFrame,
    on: str,
    fill_col: str,
    fill_val: str = 'UNKNOWN'
) -> pd.DataFrame:
    '''
    left merge two df setting null values to fixed string
    '''
    df = pd.merge(left_df, right_df, on=on, how='left')
    df[fill_col] = df[fill_col].fillna(fill_val)
    return df
