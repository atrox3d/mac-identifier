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


def get_dhcp_table(
    df:pd.DataFrame,
    # ip_column:int|str,
    mac_column:int|str,
    mac_sep:str,
    mac_replace_sep:str=':'
) -> pd.DataFrame:
    """
    Extracts and cleans IP and MAC columns from a DataFrame.
    
    Args:
        ip_column: Name (str) or index (int) of the IP column.
        mac_column: Name (str) or index (int) of the MAC column.
    """
    # --- Robust Column Selection ---
    # Validate and resolve column identifiers to actual names, providing clear errors.
    # column_names = []
    # for i, col_ref in enumerate([ip_column, mac_column]):
    #     col_type_str = "IP" if i == 0 else "MAC"
    #     try:
    #         if isinstance(col_ref, int):
    #             column_name = df.columns[col_ref]
    #         elif isinstance(col_ref, str):
    #             if col_ref not in df.columns:
    #                 raise KeyError(f"Column name '{col_ref}' not found in {list(df.columns)}")
    #             column_name = col_ref
    #         else:
    #             raise TypeError(f"Identifier must be an int or str, not {type(col_ref).__name__}.")
    #         column_names.append(column_name)
    #     except (IndexError, KeyError, TypeError) as e:
    #         raise ValueError(f"Invalid {col_type_str} column identifier provided.") from e

    # if column_names[0] == column_names[1]:
    #     raise ValueError(f"IP and MAC columns cannot be the same: '{column_names[0]}'")
    
    # Select the desired columns and explicitly create a copy.
    # This prevents the pandas SettingWithCopyWarning, which occurs when
    # modifying a slice of a DataFrame whose state (view vs. copy) is ambiguous.
    # By using .copy(), we guarantee we are working with a new, independent DataFrame.
    # df = df.copy()
    
    # ip_col, mac_col = column_names
    mac_col = df.columns[mac_column] if isinstance(mac_column, int) else mac_column
    df[mac_col] = df[mac_col].str.replace(
        mac_sep,
        mac_replace_sep,
        regex=False
    )
    return df
