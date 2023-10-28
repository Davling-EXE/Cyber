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


def decryptencrypt(string):
    if string == "decrypt":
        file = open("encrypted_msg.txt", "r")
        decrypted_text = file.read()
        print(decrypted_text)
        print(decrypt(decrypted_text))
        decryptencrypt(input("decrypt or encrypt (dont decrypt unless you have encrypted something)"))
    elif string == "encrypt":
        string = input("type a message to encrypt")
        encrypt(string)
        decryptencrypt(input("decrypt or encrypt (dont decrypt unless you have encrypted something)"))
    else:
        print("invalid command, try again")
        decryptencrypt(input("decrypt or encrypt (dont decrypt unless you have encrypted something)"))


def decrypt(string):
    """
    :param string:
    :return:
    """
    decrypt_dict = {
        "56": "A",
        "57": "B",
        "58": "C",
        "59": "D",
        "40": "E",
        "41": "F",
        "42": "G",
        "43": "H",
        "44": "I",
        "45": "J",
        "46": "K",
        "47": "L",
        "48": "M",
        "49": "N",
        "60": "O",
        "61": "P",
        "62": "Q",
        "63": "R",
        "64": "S",
        "65": "T",
        "66": "U",
        "67": "V",
        "68": "W",
        "69": "X",
        "10": "Y",
        "11": "Z",
        "12": "a",
        "13": "b",
        "14": "c",
        "15": "d",
        "16": "e",
        "17": "f",
        "18": "g",
        "19": "h",
        "30": "i",
        "31": "j",
        "32": "k",
        "33": "l",
        "34": "m",
        "35": "n",
        "36": "o",
        "37": "p",
        "38": "q",
        "39": "r",
        "90": "s",
        "91": "t",
        "92": "u",
        "93": "v",
        "94": "w",
        "95": "x",
        "96": "y",
        "97": "z",
        "98": " ",
        "99": ",",
        "100": ".",
        "101": ";",
        "102": "'",
        "103": "?",
        "104": "!",
        "105": ":"
    }
    temp = ""
    decrypted_line = ""
    for i in string:
        if i != " ":
            temp += i
        elif i == " ":
            decrypted_line += decrypt_dict[temp]
            temp = ""
    return decrypted_line


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
        "j": 31,
        "k": 32,
        "l": 33,
        "m": 34,
        "n": 35,
        "o": 36,
        "p": 37,
        "q": 38,
        "r": 39,
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
        ":": 105,
        "": ""
    }
    file = open("encrypted_msg.txt", "w")
    for i in string:
        file.write(str(encrypt_dict[i]) + " ")
    file.close()


def main():
    """
    main function
    """
    decryptencrypt(input("decrypt or encrypt (dont decrypt unless you have encrypted something)"))


    string = input("type a message to encrypt")
    encrypt(string)


if __name__ == '__main__':
    main()
