def ETL_process(curs):
    '''main ETL process'''
    with open('sql_scripts/INCREMENTAL.sql','r').read().split(";") as inc:
        for i in inc:
        	curs.execute( i )