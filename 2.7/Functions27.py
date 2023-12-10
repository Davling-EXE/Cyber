"""
author - nadav
date   - 03/11/23
functions for 2.7
"""
import glob
import os
import shutil
import subprocess
from PIL import ImageGrab
import base64

"""
constants
"""


def dir_command(main_dir):
    """
    returns a list with all the items in the given address
    :param main_dir:
    :return file_list: list with items in directory given
    """
    file_list = glob.glob(main_dir + r'\*.*')
    return file_list


def delete_command(main_dir):
    """
    deletes the item in the given address
    :param main_dir:
    :return:
    """
    os.remove(main_dir)


def copy_command(to_dir, from_dir):
    """
    copies the item in from_dir to to_dir
    :param to_dir:
    :param from_dir:
    :return: whether the command worked (bool)
    """
    shutil.copy(from_dir, to_dir)
    f = open(from_dir, "r")
    from_contents = f.read()
    f.close()
    f = open(to_dir, "r")
    to_contents = f.read()
    f.close()
    if to_contents == from_contents:
        return True
    else:
        return False


def execute_command(main_dir):
    """
    executes an exe file at the given address
    :param main_dir:
    :return: whether the command worked (bool)
    """
    if subprocess.call(main_dir) == 0:
        return True
    else:
        return False


def screenshot_command():
    """
    takes a screenshot and saves it as screenshot.jpg
    :return:
    """
    image = ImageGrab.grab()
    image.save(r"screenshot.jpg")


def get_photo_path():
    """
    send back the address of the screenshot taken by screenshot_command
    :return: file path
    """
    return r"C:\CyberWorkspace\2.7\screenshot.jpg"


def send_photo_command():
    """
    send
    :return:
    """
    with open('screenshot.jpg', 'rb') as img:
        return base64.b64encode(img.read())


def main():
    file_list = dir_command(r'C:\WS')
    for i in file_list:
        print(i)
    delete_command(r'C:\Users\nadav\OneDrive\Desktop\to_copy.txt')
    to_dir = r"C:\Users\nadav\OneDrive\Desktop\to_copy.txt"
    from_dir = r"C:\Users\nadav\OneDrive\Desktop\from_copy.txt"
    print(copy_command(to_dir, from_dir))
    execute_command(r"C:\Program Files\Notepad++\notepad++.exe")
    screenshot_command()


if __name__ == '__main__':
    main()
