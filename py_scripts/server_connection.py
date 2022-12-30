import jaydebeapi as jdba

# Установка соединения с сервером
def server_connection():
    conn = jdba.connect(
    'oracle.jdbc.driver.OracleDriver',
    'jdbc:oracle:thin:user/password@de-oracle.chronosavant.ru:1521/deoracle',
    ['user','password'],
    '/home/demipt/ojdbc8.jar'
    )
    curs = conn.cursor()
    return curs