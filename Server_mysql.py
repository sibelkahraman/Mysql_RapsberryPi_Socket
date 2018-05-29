from mysql.connector import connection
import socket
import json

class Connection:
    
    def mysql_connection(self):
        mysql_connection = connection.MySQLConnection(user='my_user',
                                                      password='1qaz2wsx3edc4rfv',
                                                      host='localhost', database='my_database')
        cursor = mysql_connection.cursor()
        # create_table = 'CREATE TABLE IF NOT EXISTS machine(record_no INT, store_no INT, data TEXT)'
        create_table = 'CREATE TABLE machine(record_no INT, store_no INT, data TEXT)'
        cursor.execute(create_table)
        mysql_connection.commit()
        mysql_connection.close()
        
    def socket_connection(self):
        host = '10.20.3.83'
        port = 34000
        sockett = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockett.bind((host, port))
        sockett.listen(1)
        connection, address = sockett.accept()
        print('Connected by ', address)
        boolean = 'true'
        while boolean:
            values = connection.recv(4096)
            datum = json.loads(values)
            if datum[0] > 0:
                self.insert_value(datum)
            if values:
                print(datum[0])
                print(type(datum[0]))
                if datum[0] == -1 :
                    connection.send(values)
                    connection.close()
                    break
                print(boolean)
            connection.send(values)
            sockett.listen(1)
            connection, address = sockett.accept()
        connection.close()
        print('finish')
        
    def insert_value(self, values):
        mysql_connection = connection.MySQLConnection(user='my_user',
                                                      password='1qaz2wsx3edc4rfv',
                                                      host='localhost', database='my_database')
        cursor = mysql_connection.cursor()
        insert_table = """INSERT INTO machine (record_no, store_no, data)
                                               VALUES(%s, %s, %s)"""
        datum = (values[0], values[1], values[3])
        print(values[0])
        cursor.execute(insert_table, datum)
        mysql_connection.commit()
        mysql_connection.close()

a = Connection()    
b = a.mysql_connection()
c = a.socket_connection()
