from pathlib import Path

from dotenv import dotenv_values
from typer import Typer

from db import csv


app = Typer()

@app.command()
def main(
    secret_dir:str=None,            # overrides SECRET_DIR
    router_filename:str=None,       # overrides ROUTER_DHCP_FILENAME
    known_macs_filename:str=None,   # overrides KNOWN_MACS_FILENAME
    unknown_macs_filename:str=None  # overrides UNKNOWN_MACS_FILENAME
):
    # try to load .env
    if Path(".env").exists():
        CONFIG = dotenv_values(".env")
    else:
        raise FileNotFoundError(".CONFIG file not found")

    # try to evaluate config
    try:
        SECRET_DIR            = secret_dir or CONFIG['SECRET_DIR']
        SECRET_PATH           = Path(SECRET_DIR).resolve()

        ROUTER_DHCP_FILENAME  = router_filename or CONFIG['ROUTER_DHCP_FILENAME']
        ROUTER_DHCP_PATH      = SECRET_PATH / ROUTER_DHCP_FILENAME

        KNOWN_MACS_FILENAME   = known_macs_filename or CONFIG['KNOWN_MACS_FILENAME']
        KNOWN_MACS_PATH       = SECRET_PATH / KNOWN_MACS_FILENAME

        UNKNOWN_MACS_FILENAME = unknown_macs_filename or  CONFIG['UNKNOWN_MACS_FILENAME']
        UNKNOWN_MACS_PATH     = SECRET_PATH / UNKNOWN_MACS_FILENAME
    except KeyError as ke:
        # could not resolve a particular config value
        print(f'cannot resolve value for config key {ke}')
        exit(1)
    
    # build router dhcp table
    router_dhcp_df = csv.load_csv(ROUTER_DHCP_PATH)
    router_dhcp_df = csv.build_mac_ref_table(router_dhcp_df, descr_col=0, mac_col=1, sep=':', replace=':', name_col_name='ip')

    # build known macs table
    known_macs_df = csv.load_csv(KNOWN_MACS_PATH, separator=';')
    known_macs_df = csv.build_mac_ref_table(known_macs_df, descr_col=1, mac_col=0, sep='-', replace=':')

    # build unknown macs table
    unknown_macs_df = csv.load_csv(UNKNOWN_MACS_PATH, separator=';')
    unknown_macs_df = csv.build_mac_ref_table(unknown_macs_df, descr_col=1, mac_col=0, sep='-', replace=':')
    
    # build stacked macs table
    stacked = csv.stack_mac_ref_tables(known_macs_df, unknown_macs_df)

    # resolve macs
    merged = csv.merge_and_fill(
        router_dhcp_df, 
        stacked, 
        on='mac', fill_col='name'
    )
    print(merged)



if __name__ == "__main__":
    # main()
    #
    app()