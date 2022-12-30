# ETL
def ETL_process(curs):
    inc = open('sql_scripts/INCREMENTAL.sql','r').read().split(";")
    for i in inc:
    	curs.execute( i )