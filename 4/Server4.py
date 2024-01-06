"""
HTTP Server Shell
Author: Barak Gonen, Nir Dweck and nadav cohen
Purpose: Provide a server or Ex.4
Usage: Fill the missing functions and constants
"""
# TO DO: import modules
import socket
import os

# TO DO: set constants
 
QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 2
DEFAULT_URL = 'index.html'
REDIRECTION_DICTIONARY = {
    "webroot/moved": "HTTP/1.1 302 Found\r\nLocation: http://127.0.0.1\r\n\r\n",
    "webroot/forbidden": "HTTP/1.1 403 Forbidden\r\n\r\n",
    "webroot/error": "HTTP/1.1 500 Error\r\n\r\n",
    "webroot/": "HTTP/1.1 200 OK\r\nContent-type: text/html;charset=utf-8\r\nContent-length: 25592\r\n\r\n",
    404: "HTTP/1.1 404 Not Found\r\n\r\n",
    400: "HTTP/1.1 400 Bad Request\r\n\r\n",
    200: "HTTP/1.1 200 OK\r\n"

}
MAX_PACKET = 1024


def get_file_data(file_name):
	"""
	Get data from file
	:param file_name: the name of the file.
	:return: file data in a string
	"""
	if not os.path.isfile(file_name):  # if file is not found in the directory, return 404 not found
		return 404
	with open(file_name, "rb") as file:  # open the file, read it all as binary data and return the data
		data = file.read()
	return data


def handle_client_request(resource, client_socket):
	"""
	Check the required resource, generate proper HTTP response and send
	to client
	:param resource: the required resource
	:param client_socket: a socket for the communication with the client
	:return: None
	"""
	""" """
	uri = "webroot/" + resource
	if uri in REDIRECTION_DICTIONARY:  # check if the url is special (error, moved...) and act accordingly
		if resource == "moved":
			client_socket.send(REDIRECTION_DICTIONARY[uri].encode())
		elif resource == "forbidden":
			with open("webroot/imgs/forbidden.jpg", "rb") as file:
				client_socket.send(REDIRECTION_DICTIONARY[uri].encode() + file.read())
		elif resource == "error":
			with open("webroot/imgs/Error.jpg", "rb") as file:
				client_socket.send(REDIRECTION_DICTIONARY[uri].encode() + file.read())
		elif resource == "":
			with open("webroot/index.html", "rb") as file:
				client_socket.send(REDIRECTION_DICTIONARY[uri].encode() + file.read())
	else:
		file_type = resource.split(".")[-1]  # take file type from file
		if file_type == 'html':  # generate type headers
			http_header = "Content-type: text/html; charset=utf-8"
		elif file_type == 'jpg':
			http_header = "Content-type: image/jpg"
		elif file_type == 'css':
			http_header = "Content-type: text/css"
		elif file_type == 'js':
			http_header = "Content-type: text/javascript; charset=UTF-8"
		elif file_type == 'txt':
			http_header = "Content-type: text/plain"
		elif file_type == 'ico':
			http_header = "Content-type: image/x-icon"
		elif file_type == 'gif':
			http_header = "Content-type: image/jpg"
		elif file_type == 'png':
			http_header = "Content-type: image/jpg"
		else:  # if there is no file type or it is invalid, return 404 no found
			client_socket.send(REDIRECTION_DICTIONARY[404].encode())
			return
		data = get_file_data(uri)

		if data == 404:
			client_socket.send(REDIRECTION_DICTIONARY[data].encode())
			return
		else:
			http_header += "\r\nContent-length: " + str(len(data)) + "\r\n\r\n"  # generate length header
			http_response = REDIRECTION_DICTIONARY[200].encode() + http_header.encode() + data  # encode 200 ok message
			client_socket.send(http_response)


def validate_http_request(request):
	"""
	Check if request is a valid HTTP request and returns TRUE / FALSE and
	the requested URL
	:param request: the request which was received from the client
	:return: a tuple of (True/False - depending if the request is valid,
	the requested resource )
	"""
	request_split = request.split(" ")
	if len(request_split) != 3 or request_split[0] != "GET" or request_split[1][0] != "/" \
		or request_split[2] != "HTTP/1.1":  # check if the request is valid and has no double spaces
		return False, ""
	return True, request_split[1][1::]  # returns True and the uri (except the first /)


def handle_client(client_socket):
	"""
	Handles client requests: verifies client's requests are legal HTTP, calls
	function to handle the requests
	:param client_socket: the socket for the communication with the client
	:return: None
	"""
	print('Client connected')
	client_request = ""
	while True:
		client_request += client_socket.recv(1).decode()
		if "\r\n\r\n" in client_request:  # run until receives \r\n\r\n, which is the end of a GET request
			break
		if client_request == '':  # break the loop in case of an error (recv returning nothing) and close the socket
			return
	valid_http, resource = validate_http_request(client_request.split("\r\n")[0])
	if valid_http:
		print('Got a valid HTTP request')
		handle_client_request(resource, client_socket)
	else:
		with open("webroot/imgs/badrequest.jpg", "rb") as file:
			client_socket.send(REDIRECTION_DICTIONARY[400].encode() + file.read())
		return

	print('Closing connection')


def main():
	# Open a socket and loop forever while waiting for clients
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		server_socket.bind((IP, PORT))
		server_socket.listen(QUEUE_SIZE)
		print("Listening for connections on port %d" % PORT)

		while True:
			client_socket, client_address = server_socket.accept()
			try:
				print('New connection received')
				client_socket.settimeout(SOCKET_TIMEOUT)
				handle_client(client_socket)
			except socket.error as err:
				print('received socket exception - ' + str(err))
			finally:
				client_socket.close()
	except socket.error as err:
		print('received socket exception - ' + str(err))
	finally:
		server_socket.close()


if __name__ == "__main__":
	# Call the main handler function
	assert get_file_data("test.txt") == b'Hand Grenade of Antioch'
	assert validate_http_request("GET / HTTP/1.1") == (True, "")
	assert validate_http_request("GET  / HTTP/1.1") == (False, "")
	assert validate_http_request("GET /abcd HTTP/1.1") == (True, "abcd")
	assert validate_http_request("GET HTTP/1.1") == (False, "")
	main()
