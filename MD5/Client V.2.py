"""
author - nadav cohen
date   - 05/10/24
MD5 brute force client
"""

import threading
import socket
import os
import hashlib

"""
constants
"""

SERVER_IP = "127.0.0.1"
PORT = 8820


class Client:
    def __init__(self):
        self.my_socket = None
        self.done = False
        self.solution = None
        self.threads = None
        self.to_decode = None
        self.lock = threading.Lock()

    def check_num(self):
        """
        brute forces within a given range
        :return:
        """
        start = int(self.my_socket.recv(10).decode())
        end = start + 9999
        start = str(start).zfill(10)
        end = str(end).zfill(10)
        cur = start
        while True:
            if int(end) < int(cur):
                return
            elif self.to_decode == hashlib.md5(cur.encode()).hexdigest():
                self.done = True
                self.solution = cur
                print(cur)
                return
            else:
                cur = int(cur) + 1
                cur = str(cur).zfill(10)

    def main(self):
        """
        the main function that starts the client and closes it as needed
        :return:
        """
        try:
            self.my_socket = socket.socket()
            self.my_socket.connect((SERVER_IP, PORT))
            self.to_decode = self.my_socket.recv(32).decode()
            while True:
                if self.my_socket.recv(1).decode() == "0":
                    if not self.done:
                        self.my_socket.send("cont".encode())
                        core_count = str(os.cpu_count()).zfill(2)
                        self.my_socket.send(core_count.encode())
                        self.threads = []
                        for i in range(os.cpu_count()):
                            self.threads.append(threading.Thread(target=self.check_num))
                            self.threads[i].start()
                        while threading.active_count() > 4:
                            pass
                    else:
                        self.my_socket.send("done".encode())
                        self.my_socket.send(self.solution.encode())
                        self.my_socket.close()
                        break
                else:
                    self.done = True
                    self.my_socket.close()
                    break

        except socket.error as err:
            print(err)


if __name__ == '__main__':
    client = Client()
    client.main()
