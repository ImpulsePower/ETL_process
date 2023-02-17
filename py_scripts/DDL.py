"""Python Libraries"""
from os 		import chdir
from jaydebeapi import connect

def DDL ():
	'''Auxiliary script for creating tables'''
	conn = connect(
	'oracle.jdbc.driver.OracleDriver',
	'jdbc:oracle:thin:demipt/password@de-oracle.chronosavant.ru:1521/deoracle',
	['demipt','password'],
	'/home/demipt/ojdbc8.jar'
	)

	curs = conn.cursor()

	chdir('/home/demipt/yupi')

	with open('sql_scripts\DDL_DWH.sql').read().split(";") as DWH:
		for i in DWH:
			curs.execute( i )

	with open('sql_scripts\DDL_STG.sql').read().split(";") as STG:
		for j in STG:
			curs.execute( j )

	with open('sql_scripts\DDL_REP_META.sql').read().split(";") as REP_META:
		for k in REP_META:
			curs.execute( k )