"""Final step"""
def close_server_connection(curs,conn):
    """Закрытие соединения"""
    curs.close()
    conn.close()
