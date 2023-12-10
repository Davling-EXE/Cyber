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
    :return: the message with the length as the first 4 bytes
    """
    length = str(len(data))
    zfill_length = length.zfill(4)
    message = zfill_length + data
    return message


def create_msg_byte(data):
    """
    creates a message following the protocol with a length field (byte)
    :param data:
    :return: the message with the length as the first 7 bytes
    """
    length = str(len(data))
    zfill_length = bytes(length.zfill(7), 'utf-8')
    message = zfill_length + data
    return message


def get_msg(my_socket):
    """
    Extract message from protocol, without message length
    :param my_socket:
    :return:
    """
    len_word = my_socket.recv(4).decode()
    if len_word.isnumeric():
        message = my_socket.recv(int(len_word)).decode()
        return True, message
    else:
        return False, "Error"


def get_msg_byte(my_socket):
    """
    Extract message from protocol, without message length
    :param my_socket:
    :return:
    """
    len_word = my_socket.recv(7).decode()
    if len_word.isnumeric():
        message = my_socket.recv(int(len_word))
        return True, message
    else:
        return False, "Error"


def main():
    print("hello")


if __name__ == '__main__':
    main()
