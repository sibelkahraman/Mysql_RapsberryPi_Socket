import socket

class MySocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, hostt, portt):
        self.sock.connect((hostt, portt))

    def my_send(self, msg):
        total_sent = 0
        while total_sent < len(msg):
            sent = self.sock.send(msg[total_sent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_sent = total_sent + sent
            print(total_sent)

    def my_receive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < 15:
            chunk = self.sock.recv(2048)
            print(chunk)
            if chunk == '':
                raise RuntimeError("Socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
            while self.sock.recv(2048) != "ack":
                print('ack waiting')
            print('ack accessed')

        return ''.join(chunks)
        print(chunks)


host = "10.20.3.83"
port = 34000
server = MySocket()
server.connect(host, port)
server.my_send("hello")
server.my_receive()
