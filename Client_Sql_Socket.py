import socket
import threading
import json
from mysql.connector import connection
mutex = threading.Lock()


class SqlConnection:
    def __init__(self):
        pass

    def create_connection(self, record_no):
        sql_connection = connection.MySQLConnection(user='root',
                                                    password='1qaz2wsx3edc4rfv',
                                                    host='localhost', database='data')  # create sql connection
        cursor = sql_connection.cursor()
        table = 'CREATE TABLE IF NOT EXISTS machine(record_no INT, store_no INT,machine_no INT, data TEXT, ack TEXT)'
        cursor.execute(table)
        mutex.acquire()
        insert_query = """INSERT INTO machine 
                            (record_no, store_no, machine_no, data, ack) 
                             VALUES(%s, %s, %s, %s, %s)"""

        values = (record_no, 1, 2, 'false', 'false')
        if record_no > 0:
            cursor.execute(insert_query, values)
        mutex.release()
        sql_connection.commit()
        sql_connection.close()
        socket_connect = SocketConnection()
        socket_thread = threading.Thread(target=socket_connect.create_connection(values))
        socket_thread.start()
        socket_thread.join()

    def update_database(self, record_no):
        sql_connection = connection.MySQLConnection(user='root',
                                                    password='1qaz2wsx3edc4rfv', host='localhost', database='data')
        cursor = sql_connection.cursor()
        if record_no > 0:
            mutex.acquire()
            update_query = """UPDATE machine SET ack=%s WHERE record_no=%s"""
            values = ('true', record_no)
            cursor.execute(update_query, values)
            sql_connection.commit()
            sql_connection.close()
            mutex.release()
        elif record_no < 0:
            sql_connection.close()


class SocketConnection:
    def __init__(self):
        pass

    def create_connection(self, values):
        host = "10.20.3.83"  # server ip
        port = 34000
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        message = json.dumps(values)  # Serializing Data
        print(values)
        sock.send(message)  # send data that already serialize

        if values[0] > 0:  # if first data small than 0 it means there is no data to receive
            data = sock.recv(4096)  # take data from server
            ack = json.loads(data)  # load data
            sock.close()
            print(ack[0])
            print(type(ack[0]))
            sql_ack = SqlConnection()
            ack_thread = threading.Thread(name='ack', target=sql_ack.update_database(ack[0]))
            ack_thread.start()
            ack_thread.join()
        else:
            sock.close()


t = 1
while 1:
    connect = SqlConnection()
    sql = threading.Thread(name='Sql_Connection', target=connect.create_connection(t))
    sql.start()
    sql.join()
    t = t + 1
    if t > 15:
        sql = threading.Thread(name='Sql_Connection', target=connect.create_connection(-1))
        break
