"""Python Libraries"""
from pandas import read_excel, Series

def load_data_from_terminals(X, DT, curs):
    '''Downloading data from terminals'''
    df = read_excel( 'terminals_' + X + '.xlsx', sheet_name='terminals', header=0, index_col=None )
    df['create_dt'] = Series(DT, index=df.index)
    curs.executemany( """insert into DEMIPT.YUPI_STG_TERMINALS ( TERMINAL_ID, TERMINAL_TYPE, TERMINAL_CITY, TERMINAL_ADDRESS, CREATE_DT ) values ( ?, ?, ?, ?, to_date(?,'YYYY-MM-DD')) """, df.values.tolist() )
