"""Python Libraries"""
from jaydebeapi import connect

def server_connection():
    '''Establishing a connection to the server'''
    conn = connect(
    'oracle.jdbc.driver.OracleDriver',
    'jdbc:oracle:thin:user/password@de-oracle.chronosavant.ru:1521/deoracle',
    ['user','password'],
    '/home/demipt/ojdbc8.jar'
    )
    curs = conn.cursor()
    return curs
