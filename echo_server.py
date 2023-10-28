"""
author - cyber
date   - 29/11/17
socket server
"""
import socket
import struct

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
                comm_socket.send(comm_socket.recv(MAX_PACKET))
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