from os                                     import chdir, path
from py_scripts.server_connection           import server_connection
from py_scripts.find_early_date             import find_early_date
from py_scripts.load_data_from_terminals    import load_data_from_terminals
from py_scripts.load_transactions           import load_transactions
from py_scripts.load_blacklist              import load_blacklist
from py_scripts.ETL_process                 import ETL_process
from py_scripts.report_1                    import report_1
from py_scripts.report_2                    import report_2
from py_scripts.report_3                    import report_3
from py_scripts.report_4                    import report_4
from py_scripts.file_transfer               import file_transfer
from py_scripts.close_server_connection     import close_server_connection

def main():
    cursor, connection = server_connection()
    chdir('/home/demipt/yupi')
    X, date = find_early_date()
    load_data_from_terminals(X, date, cursor)
    load_transactions(X, cursor)
    load_blacklist(X, date, cursor)
    ETL_process(cursor)
    report_1(cursor, date)
    report_2(cursor, date)
    report_3(cursor, date)
    report_4(cursor, date)
    file_transfer(X)
    close_server_connection(cursor, connection)

# Profiler + run
if path.isfile('profiler.py'):
    from profiler import go
    go()
if __name__ == '__main__':
    main()