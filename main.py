from pathlib import Path

from dotenv import dotenv_values
from typer import Typer

from db import csv


app = Typer()

@app.command()
def main(
    secret_dir:str=None,
    router_filename:str=None,
    known_macs_filename:str=None,
    unknown_macs_filename:str=None
):
    if Path(".env").exists():
        CONFIG = dotenv_values(".env")
    else:
        raise FileNotFoundError(".CONFIG file not found")

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
        print(f'cannot resolve value for config key {ke}')
        exit(1)
    
    router_dhcp_df = csv.load_csv(ROUTER_DHCP_PATH)
    router_dhcp_df = csv.build_mac_ref_table(router_dhcp_df, descr_col=0, mac_col=1, sep=':', replace=':', name_col_name='ip')
    # print(router_dhcp_df)

    known_macs_df = csv.load_csv(KNOWN_MACS_PATH, separator=';')
    known_macs_df = csv.build_mac_ref_table(known_macs_df, descr_col=1, mac_col=0, sep='-', replace=':')
    # print(known_macs_df)

    unknown_macs_df = csv.load_csv(UNKNOWN_MACS_PATH, separator=';')
    unknown_macs_df = csv.build_mac_ref_table(unknown_macs_df, descr_col=1, mac_col=0, sep='-', replace=':')
    # print(unknown_macs_df)
    
    stacked = csv.stack_mac_ref_tables(known_macs_df, unknown_macs_df)
    # print(stacked)

    merged = csv.merge_and_fill(
        router_dhcp_df, 
        stacked, 
        on='mac', fill_col='name')
    # print(merged.columns)
    print(merged)



if __name__ == "__main__":
    # main()
    #
    app()