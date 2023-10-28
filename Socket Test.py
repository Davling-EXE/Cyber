import socket

SERVER_IP = "127.0.0.1"
PORT = 8820
MAX_PACKAGE = 1024


def main():
    my_socket = socket.socket()

    try:
        my_socket.connect((SERVER_IP, PORT))

        my_socket.send(input("Enter your name: ").encode())

        data = my_socket.recv(MAX_PACKAGE).decode()
        print("The server sent " + data)

    except socket.error as err:
        print(err)

    finally:
        my_socket.close()


if __name__ == '__main__':
    main()