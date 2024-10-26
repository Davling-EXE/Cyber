"""
author - nadav
date   - 05/10/24
MD5 brute force server
"""
import socket
import hashlib
import threading

"""
constants
"""

IP = '0.0.0.0'
PORT = 8820
QUEUE_SIZE = 1


class Server:
    def __init__(self, to_decode):
        self.server_socket = None
        self.to_decode = to_decode
        self.cur = "0000000000"
        self.lock = threading.Lock()
        self.done = False
        self.solution = "Hasn't found yet"

    def handle_client(self, client_socket):
        """
        this sends the data to be decoded by the client and the ranges it should check
        :param client_socket:
        :return:
        """
        client_socket.send(self.to_decode.encode())
        while not self.done:
            client_socket.send("0".encode())
            state = client_socket.recv(4).decode()
            if state == "done":
                self.solution = client_socket.recv(10).decode()
                self.done = True
            elif state == "cont":
                num_of_cores = int(client_socket.recv(2).decode())
                for i in range(num_of_cores):
                    with self.lock:
                        client_socket.send(self.cur.encode())
                        self.cur = str(int(self.cur) + 10000).zfill(10)
        client_socket.send("1".encode())

    def recieve_client(self):
        """
        handles receiving each client and assigning a thread to handle it
        :return:
        """
        while not self.done:
            client_socket, client_address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def main(self):
        """
        the main that starts the server and closes it when it's done
        :return:
        """
        self.server_socket = socket.socket()
        self.server_socket.bind(("0.0.0.0", 8820))
        self.server_socket.listen()
        print("Server is up and running")
        threading.Thread(target=self.recieve_client).start()
        while True:
            if not self.solution == "Hasn't found yet":
                print("the original number is: " + self.solution)
                self.server_socket.close()
                break
        return


if __name__ == '__main__':
    server = Server(hashlib.md5(b"0003500000").hexdigest())
    server.main()
