'''Final step'''
def close_server_connection(curs,conn):
    '''Close connection'''
    curs.close()
    conn.close()
