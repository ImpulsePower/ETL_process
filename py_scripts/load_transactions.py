"""Python Libraries"""
from pandas import read_csv

def load_transactions(X, curs):
    '''Downloading transaction data'''
    df = read_csv( 'transactions_' + X + '.txt', sep = ";", header = 0, index_col = None )
    df = df.reindex(columns=['transaction_id', 'transaction_date', 'card_num', 'oper_type', 'amount', 'oper_result', 'terminal'])
    df['transaction_date'] = df['transaction_date'].astype(str)
    curs.executemany( """insert into DEMIPT.YUPI_STG_TRANSACTIONS ( TRANS_ID, TRANS_DATE, CARD_NUM, OPER_TYPE, AMT, OPER_RESULT, TERMINAL ) values ( ?, to_date(?,'YYYY-MM-DD HH24:MI:SS'), ?, ?, ?, ?, ?) """, df.values.tolist() )
