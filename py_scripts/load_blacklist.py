"""Python Libraries"""
from pandas import read_excel

def load_blacklist(X, DT, curs):
    '''Downloading data from the "BlackList" of passports'''
    df = read_excel( 'passport_blacklist_' + X + '.xlsx', sheet_name='blacklist', header=0, index_col=None )
    df = df.dropna(how='any',axis=0)
    df = df.loc[df['date'] == DT]
    df['date'] = df['date'].astype(str)
    df = df.reindex(columns=['passport', 'date'])
    curs.executemany( """insert into DEMIPT.YUPI_STG_PASSPORT_BLACKLIST ( PASSPORT_NUM, ENTRY_DT ) values ( ?, to_date(?,'YYYY-MM-DD')) """, df.values.tolist() )
