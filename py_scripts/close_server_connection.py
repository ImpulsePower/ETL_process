# Закрытие соединения
def close_server_connection(curs,conn):
    curs.close()
    conn.close()