import os
import jaydebeapi as jdba

# Установка соединения с сервером
conn = jdba.connect(
'oracle.jdbc.driver.OracleDriver',
'jdbc:oracle:thin:demipt/gandalfthegrey@de-oracle.chronosavant.ru:1521/deoracle',
['demipt','gandalfthegrey'],
'/home/demipt/ojdbc8.jar'
)

curs = conn.cursor()

os.chdir('/home/demipt/yupi')

DWH = open('sql_scripts\DDL_DWH.sql').read().split(";")
for i in DWH:
	curs.execute( i )

STG = open('sql_scripts\DDL_STG.sql').read().split(";")
for j in STG:
	curs.execute( j )

REP_META = open('sql_scripts\DDL_REP_META.sql').read().split(";")
for k in REP_META:
	curs.execute( k )