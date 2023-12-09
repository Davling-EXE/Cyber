"""
author - nadav
date   - 03/11/23
exercise 2.7 client
"""

"""
constants
"""


def create_msg(data):
    """
    creates a message following the protocol with a length field
    :param data:
    :return: the message with the length as the first 3 bytes
    """
    length = str(len(data))
    zfill_length = length.zfill(3)
    message = zfill_length + data
    return message


def get_msg(my_socket):
    """
    Extract message from protocol, without message length
    :param my_socket:
    :return:
    """
    len_word = my_socket.recv(3).decode()
    if len_word.isnumeric():
        message = my_socket.recv(int(len_word)).decode()
        return True, message
    else:
        return False, "Error"


def main():
    print("hello")


if __name__ == '__main__':
    main()
