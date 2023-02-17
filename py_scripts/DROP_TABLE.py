"""Python Libraries"""
from os 		import chdir
from jaydebeapi import connect

def DROP ():
	'''Auxiliary script for droping tables'''
	# Установка соединения с сервером
	conn = connect(
	'oracle.jdbc.driver.OracleDriver',
	'jdbc:oracle:thin:demipt/password@de-oracle.chronosavant.ru:1521/deoracle',
	['demipt','password'],
	'/home/demipt/ojdbc8.jar'
	)
	curs = conn.cursor()

	chdir('/home/demipt/yupi')

	with open('sql_scripts\DROP_TABLE.sql').read().split(";") as DROP:
		for i in DROP:
			curs.execute( i )