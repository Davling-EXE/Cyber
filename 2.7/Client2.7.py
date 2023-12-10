"""
author - nadav
date   - 03/11/23
exercise 2.7 client
"""
import Protocol27
import socket
import base64
from PIL import Image
from io import BytesIO
import logging

"""
constants
"""

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/logger.log'

SERVER_IP = "127.0.0.1"
PORT = 8820
MAX_PACKAGE = 1024


def main():
    my_socket = socket.socket()
    try:
        raw_input = input("enter a command ")
        my_socket.connect((SERVER_IP, PORT))

        while raw_input != "EXIT":
            send_message = Protocol27.create_msg(raw_input)
            my_socket.send(send_message.encode())
            if raw_input == "SEND_PHOTO":
                try:
                    data = Protocol27.get_msg_byte(my_socket)[1]
                    base64str = data.decode()
                    # Decode the base64 string back to image data
                    decoded_image = base64.b64decode(base64str)

                    # Create a PIL Image object from the decoded image data
                    image = Image.open(BytesIO(decoded_image))
                    image.save('output_image.jpg')
                    image.show()
                except "failed to send" as err:
                    print(err)
            else:
                data = Protocol27.get_msg(my_socket)[1]
                if data == "Error":
                    print("Error")
                else:
                    print(data)
            raw_input = input("enter a command ")
    except socket.error as err:
        print(err)

    my_socket.close()


if __name__ == '__main__':
    main()
