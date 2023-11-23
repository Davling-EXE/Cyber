"""
author - nadav
date   - 03/11/23
exercise 2.6 client
"""
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

    while True:
        try:
            my_socket = socket.socket()
            my_socket.connect((SERVER_IP, PORT))

            user_input = input("input a command ")
            if valid_command(user_input):
                my_socket.send(user_input.encode())
                print(my_socket.recv(MAX_PACKAGE).decode())
            else:
                print("Invalid command")

        except socket.error as err:
            print(err)

        finally:
            my_socket.close()


if __name__ == '__main__':
    assert valid_command("TIME")
    assert valid_command("NAME")
    assert valid_command("RAND")
    assert valid_command("EXIT")
    assert not valid_command("HUGE")
    main()
