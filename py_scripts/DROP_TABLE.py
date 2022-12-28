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

DROP = open('sql_scripts\DROP_TABLE.sql').read().split(";")
for i in DROP:
	curs.execute( i )