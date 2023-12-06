"""
author - nadav
date   - 03/11/23
exercise 2.7 client
"""
import Protocol27
import socket

"""
constants
"""

SERVER_IP = "127.0.0.1"
PORT = 8820
MAX_PACKAGE = 1024


def valid_command(string):
    if string == "TIME" or string == "NAME" or string == "RAND" or string == "EXIT":
        return True
    else:
        return False


def main():
    my_socket = socket.socket()
    try:
        send_message = input("enter a command ")
        my_socket.connect((SERVER_IP, PORT))

        while send_message != "EXIT":
            send_message = Protocol27.create_msg(send_message)
            my_socket.send(send_message.encode())
            data = Protocol27.get_msg(my_socket)[1]
            if data == "Error":
                print("Error")
            else:
                print("The server sent " + data)
            send_message = input("enter a command ")
    except socket.error as err:
        print(err)

    my_socket.close()


if __name__ == '__main__':
    main()