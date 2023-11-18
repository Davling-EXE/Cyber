import socket

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
        my_socket.connect((SERVER_IP, PORT))
        while True:
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
    main()
