"""
author - nadav
date   - 03/11/23
exercise 2.6 client
"""
import socket
import logging
import os

"""
constants
"""

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/logger.log'
FILE_PATH = r"C:\Users\nadav\OneDrive\Desktop\Cyber Workspace\encrypted_msg.txt"

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
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)
    assert valid_command("TIME")
    assert valid_command("NAME")
    assert valid_command("RAND")
    assert valid_command("EXIT")
    assert not valid_command("HUGE")
    main()
