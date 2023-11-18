"""
author - nadav
date   - 03/11/23
exercise 2.6 server
"""
import socket
import struct
import datetime
import random

IP = '0.0.0.0'
PORT = 8820
QUEUE_SIZE = 1
MAX_PACKET = 1024


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        # endless loop to receive client after client
        while True:
            print('server is up and running')
            comm_socket, client_address = server_socket.accept()
            try:
                user_input = comm_socket.recv(4).decode()
                if user_input == "TIME":
                    comm_socket.send(datetime.datetime.now().strftime("%H:%M:%S").encode())
                elif user_input == "NAME":
                    comm_socket.send("Bofadese".encode())
                elif user_input == "RAND":
                    comm_socket.send(str(random.randint(1, 10)).encode())
                elif user_input == "EXIT":
                    comm_socket.send("client socket disconnected".encode())
                    comm_socket.close()
            except socket.error as msg:
                print('client socket disconnected- ' + str(msg))
            finally:
                comm_socket.close()
    except socket.error as msg:
        print('failed to open server socket - ' + str(msg))
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
