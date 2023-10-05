"""
Author: Nadav Cohen
Date: 10/5/2023
Description: helping romeo decrypt and encrypt his letters
"""
import logging
import os


"""
constants
"""


def encrypt(string):
    """
    :param string:
    :return:
    """

    encrypt_dict = {
        "A": 56,
        "B": 57,
        "C": 58,
        "D": 59,
        "E": 40,
        "F": 41,
        "G": 42,
        "H": 43,
        "I": 44,
        "J": 45,
        "K": 46,
        "L": 47,
        "M": 48,
        "N": 49,
        "O": 60,
        "P": 61,
        "Q": 62,
        "R": 63,
        "S": 64,
        "T": 65,
        "U": 66,
        "V": 67,
        "W": 68,
        "X": 69,
        "Y": 10,
        "Z": 11,
        "a": 12,
        "b": 13,
        "c": 14,
        "d": 15,
        "e": 16,
        "f": 17,
        "g": 18,
        "h": 19,
        "i": 30,
        "j": 30,
        "k": 30,
        "l": 30,
        "m": 30,
        "n": 30,
        "o": 30,
        "p": 30,
        "q": 30,
        "r": 30,
        "s": 90,
        "t": 91,
        "u": 92,
        "v": 93,
        "w": 94,
        "x": 95,
        "y": 96,
        "z": 97,
        " ": 98,
        ",": 99,
        ".": 100,
        ";": 101,
        "'": 102,
        "?": 103,
        "!": 104,
        ":": 105
    }
    file = open("encrypted_msg.txt", "w")
    for i in string:
        file.write(str(encrypt_dict[i]) + " ")
    file.close()


def main():
    """
    main function
    """
    encrypt("Don't waste your love on somebody, who doesn't value it.")
    file = open("encrypted_msg.txt", "r")
    print(file.read())


if __name__ == '__main__':
    main()
