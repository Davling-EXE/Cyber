"""
author - nadav
date   - 03/11/23
exercise 2.7 server
"""
import os.path
import socket
import Protocol27
import Functions27
import logging
import os

"""
constants
"""
LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/logger.log'


def main():
    server_socket = socket.socket()
    server_socket.bind(("0.0.0.0", 8820))
    logging.debug("socket bound")
    server_socket.listen()
    logging.debug("socket listen and ready to go")
    print("Server is up and running")

    logging.debug("waiting for connection")
    (client_socket, client_address) = server_socket.accept()
    logging.debug("client connected")
    print("Client connected")

    data = (Protocol27.get_msg(client_socket)[1])
    reply = ""
    reply_byte = b""

    while data != "EXIT":
        if data[:3] == "DIR":
            logging.debug("executing command")
            reply = ", ".join(Functions27.dir_command(data[4:]))
        elif data[:6] == "DELETE":
            logging.debug("executing command")
            Functions27.delete_command(data[7:])
            if os.path.exists(data[7:]):
                logging.info("command executed unsuccessfully")
                reply = "didn't delete"
            else:
                reply = data[7:] + " deleted"
        elif data[:4] == "COPY":
            both_path = data[5:]
            dir_length = 0
            f = True
            for element in both_path:
                if element != " " and f:
                    dir_length += 1
                else:
                    f = False
            from_path = both_path[:dir_length]
            to_path = both_path[dir_length+1:]
            logging.debug("executing command")
            if Functions27.copy_command(to_path, from_path):
                logging.info("command executed successfully")
                reply = "file at " + from_path + " copied to " + to_path
            else:
                logging.info("command executed unsuccessfully")
                reply = "copy failed"
        elif data[:7] == "EXECUTE":
            logging.debug("executing command")
            if Functions27.execute_command(data[8:]):
                logging.info("command executed successfully")
                reply = "program executed"
            else:
                logging.info(f"command executed unsuccessfully")
                reply = "program failed"
        elif data[:10] == "SCREENSHOT":
            logging.debug("executing command")
            Functions27.screenshot_command()
            screenshot_dir = Functions27.get_photo_path()
            if os.path.exists(screenshot_dir) and os.path.getsize(screenshot_dir) > 100000:
                logging.info("command executed unsuccessfully")
                reply = "screenshot saved at " + screenshot_dir
            else:
                logging.info("command executed unsuccessfully")
                reply = "screenshot failed "
        elif data[:10] == "SEND_PHOTO":
            logging.debug("executing command")
            reply_byte = Functions27.send_photo_command()
        else:
            logging.warning("invalid command")
            reply = "invalid command"
        if data[:10] == "SEND_PHOTO":
            client_socket.send(Protocol27.create_msg_byte(reply_byte))
        else:
            client_socket.send(Protocol27.create_msg(reply).encode())
        data = Protocol27.get_msg(client_socket)[1]
    client_socket.send(Protocol27.create_msg("Goodbye").encode())
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)
    main()
