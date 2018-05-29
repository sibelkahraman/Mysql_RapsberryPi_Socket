import socket
import threading
import time

from mysql.connector import connection
chunks = []

connection_ = connection.MySQLConnection(user='root', password='1qaz2wsx3edc4rfv', host='localhost')
cursor = connection_.cursor()
cursor.execute('DROP DATABASE IF EXISTS data')
db = 'CREATE DATABASE data'
cursor.execute(db)
connection_.commit()
connection_.close()
record_no = 0
mutex = threading.Lock()


class ChildProgram:
    def __init__(self, ready=None):
        self.ready = ready
        self.connection = None

    def connect(self):
        # lets make connection, expensive
        self.connection = MyDatabase()

        # then fire the ready event
        self.ready.set()

    def some_logic(self):
        # do something with self.connection
        pass


class MySocket:
    host = "10.20.3.83"
    port = 34000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    def __init__(self):
        pass
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # def connect(self, host, port):

    def my_send(self, msg, msg2):
        total_sent = 0
        # while total_sent < len(msg):
        self.sock.sendall(str.encode("\n".join((str(msg), str(msg2)))))
        # if sent == 0:
        #    raise RuntimeError("socket connection broken")
        # total_sent = total_sent + sent
        print(total_sent)

    def my_receive(self):
        bytes_recd = 0
        while bytes_recd < 15:
            chunk = self.sock.recv(2048)
            print(chunk)
            if chunk == '':
                raise RuntimeError("Socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        print(chunks)
        return ''.join(chunks)


class MyDatabase:
    def __init__(self):
        pass

    def write(self, a):
        mutex.acquire()
        con_db = connection.MySQLConnection(user='root', password='1qaz2wsx3edc4rfv', host='localhost', database='data')
        cursor_ex = con_db.cursor()
        table = 'CREATE TABLE IF NOT EXISTS machine(record_no INT, store_no INT,machine_no INT, data TEXT, ack TEXT)'
        cursor_ex.execute(table)
        # datum = (record_no, )
        sql_s = """INSERT INTO machine
                    (record_no, store_no, machine_no, data, ack) 
                     VALUES(%s, %s, %s, %s, %s)"""
        values = (record_no, 1, 2, 'false', 'false')
        cursor_ex.execute(sql_s, values)
        con_db.commit()
        con_db.close()
        mutex.release()
        record_no + 1

        m_d = MyDatabase()
        updater_t = threading.Thread(name="update", target=m_d.update_database())
        updater_t.start()
        updater_t.join()

    def update_database(self):
        mutex.acquire()
        con_db = connection.MySQLConnection(user='root', password='1qaz2wsx3edc4rfv', host='localhost', database='data')
        cursor_ex = con_db.cursor()
        cursor_ex.execute("UPDATE machine SET ack = false WHERE record_no = 0")
        con_db.commit()
        con_db.close()
        mutex.release()


class Functions:
    socket = MySocket()
    m_d = MyDatabase()

    def __init__(self):
        pass

    def write_function(self, a):
        m_d = MyDatabase()
        m_d.write(a)

    # def connect_function(self):
        # host = "10.20.3.83"
        # port = 34000
        # socket.connect(host, port)

    def my_send_function(self, text, record_num):
        self.socket.my_send(text, record_num)

    def update_function(self, a):
        mutex.acquire()
        connect = connection.MySQLConnection(user='root', password='1qaz2wsx3edc4rfv', host='localhost', database='data')
        cursor_ex = connect.cursor()
        time.sleep(1)
        son = cursor_ex.execute("""UPDATE machine 
                        SET ack=%s
                        WHERE record_no=%s""", ('true', 0))
        print(son)
        mutex.release()
        # cursor_ex.execute("SELECT ack FROM machine WHERE record_no = ?", (1,))
        # data = cursor_ex.fetchall()
        # while len(data) == 0:
        #    print()
        # self.m_d.update_database(a)


class CreateThread:
    host = "10.20.3.83"
    port = 34000

    def __init__(self):
        pass
    f = Functions()

    # writer_t = threading.Thread(name="database", target=m_d.write(1))
    writer_t = threading.Thread(name="database", target=f.write_function(1))

    # socket_t = threading.Thread(name="socket", target=socket.connect(host, port))
    # socket_t = threading.Thread(name="socket", target=f.connect_function())

    # sender_t = threading.Thread(name="sender", target=socket.my_send("Lost on you"))
    sender_t = threading.Thread(name="sender", target=f.my_send_function(3, 1))

    # updater_t = threading.Thread(name="update", target=m_d.update_database(1))

    # ready = threading.Event()
    # program = ChildProgram(ready)

    writer_t.start()
    # socket_t.start()
    sender_t.start()

    writer_t.join()
    # socket_t.join()
    sender_t.join()


s = Functions()

host = "10.20.3.83"
port = 34000
server = MySocket()
# server.connect(host, port)
# server.my_send("hello")
# server.my_receive()
