"""
HTTP Server Shell
Author: Barak Gonen, Nir Dweck and nadav cohen
Purpose: Provide a server or Ex.4+
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
	404: "HTTP/1.1 404 Not Found\r\n\r\n",
	400: "HTTP/1.1 400 BAD REQUEST\r\n\r\n",
	200: "HTTP/1.1 200 OK\r\n"
}
TYPE_DICTIONARY = {
	'html': "text/html;charset=utf-8",
	'jpg': "image/jpeg",
	'css': "text/css",
	'js': "text/javascript; charset=UTF-8",
	'txt': "text/plain",
	'ico': "image/x-icon",
	'gif': "image/jpeg",
	'png': "image/png"
}
MAX_PACKET = 1024
WEB_ROOT = 'webroot'


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
	if resource == '':
		uri = DEFAULT_URL
	else:
		uri = resource
	# handles calculate next command
	if resource.startswith('calculate-next?'):
		func_parts = resource.split('?')
		if '=' in func_parts[1]:
			param_val = func_parts[1].split('=')
			if len(param_val) != 2 or param_val[0] != 'num':
				client_socket.send(REDIRECTION_DICTIONARY[400].encode())
			else:
				num = param_val[1]
				calculate_next(num, client_socket)
		else:
			client_socket.send(REDIRECTION_DICTIONARY[400].encode())
	# handles calculate area command
	elif resource.startswith('calculate-area?'):
		func_parts = resource.split('?')
		if '&' in func_parts[1]:
			param_parts = func_parts[1].split('&')
			if len(param_parts) != 2:
				client_socket.send(REDIRECTION_DICTIONARY[400].encode())
			else:
				if '=' in param_parts[0] and '=' in param_parts[1]:
					part1 = param_parts[0].split('=')
					part2 = param_parts[1].split('=')
					if part1[0] != 'width' and part1[0] != 'height':
						client_socket.send(REDIRECTION_DICTIONARY[400].encode())
					elif part2[0] != 'width' and part2[0] != 'height':
						client_socket.send(REDIRECTION_DICTIONARY[400].encode())
					num1 = part1[1]
					num2 = part2[1]
					calculate_area(num1, num2, client_socket)
				else:
					client_socket.send(REDIRECTION_DICTIONARY[400].encode())
		else:
			client_socket.send(REDIRECTION_DICTIONARY[400].encode())
	# handles Get Posted Image command
	elif resource.startswith('image?'):
		func_parts = resource.split('?')
		if '=' in func_parts[1]:
			param_val = func_parts[1].split('=')
			if len(param_val) != 2 or param_val[0] != 'image-name':
				client_socket.send(REDIRECTION_DICTIONARY[400].encode())
			else:
				name = param_val[1]
				image(name, client_socket)
		else:
			client_socket.send(REDIRECTION_DICTIONARY[400].encode())

	else:
		url = 'webroot/' + uri

		if uri in REDIRECTION_DICTIONARY.keys():
			http_start_line = REDIRECTION_DICTIONARY[uri]
			client_socket.send(http_start_line.encode())
			if uri == '/moved':
				client_socket.send('Location: /\r\n'.encode())
		else:
			filename, file_extension = os.path.splitext(uri)
			file_type = file_extension[1:]
			if file_type in TYPE_DICTIONARY.keys():
				http_header = TYPE_DICTIONARY[file_type]

			data = get_file_data(url)

			if data == 404:
				client_socket.send(REDIRECTION_DICTIONARY[404].encode())
			else:
				client_socket.send(REDIRECTION_DICTIONARY[200].encode())
				response_headers = 'Content-Type:' + http_header + "\r\n"+'Content-Length:'+str(len(data)) + "\r\n\r\n"
				client_socket.send(response_headers.encode())
				client_socket.send(data)


def validate_http_request(request):
	"""
	Check if request is a valid HTTP request and returns TRUE / FALSE and
	the requested URL
	:param request: the request which was received from the client
	:return: a tuple of (True/False - depending if the request is valid,
	the requested resource )
	"""
	request_split = request.split(" ")
	if len(request_split) != 3 or (request_split[0] != "GET" and request_split[0] != "POST") \
		or request_split[1][0] != "/" or request_split[2] != "HTTP/1.1":
		# check if the request is valid and has no double spaces
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
		if "\r\n\r\n" in client_request:  # run until receives \r\n\r\n, which is the end of a request
			break
		if client_request == '':  # break the loop in case of an error (recv returning nothing) and close the socket
			return
	valid_http, resource = validate_http_request(client_request.split("\r\n")[0])
	if valid_http:
		print('Got a valid HTTP request')
		if client_request.startswith("GET"):
			handle_client_request(resource, client_socket)
		# handles Post Image command
		elif client_request.startswith("POST"):
			upload(client_request, client_socket)
	else:
		client_socket.send(REDIRECTION_DICTIONARY[400].encode())
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


def calculate_next(num, client_socket):
	"""
	Get the num from the request line, make sure it is int type
	Also sends the follow number after it (the next one)
	:param num: num from the request line
	:param client_socket: the socket for the communication with the client
	:return: None
	"""
	if not num.isnumeric():
		client_socket.send(REDIRECTION_DICTIONARY[400].encode())
	else:
		client_socket.send(REDIRECTION_DICTIONARY[200].encode())
		client_socket.send("Content-Type: text/plain\r\n".encode())
		len_heather = "Content-Length:" + str(len(str(int(num)+1))) + '\r\n\r\n'
		client_socket.send(len_heather.encode())
		client_socket.send(str(int(num) + 1).encode())


def calculate_area(width, height, client_socket):
	"""
	Get the width and the height from the request line, make sure it is int type
	Also sends the area of the triangular that consist from the width and the height
	:param width: num from the request line
	:param height: num from the request line
	:param client_socket: the socket for the communication with the client
	:return: None
	"""
	if not (width.isnumeric() and height.isnumeric()):
		client_socket.send(REDIRECTION_DICTIONARY[400].encode())
	else:
		client_socket.send(REDIRECTION_DICTIONARY[200].encode())
		client_socket.send("Content-Type: text/plain\r\n".encode())
		len_heather = "Content-Length: " + str(len(str(float(width) * float(height) / 2))) + '\r\n\r\n'
		client_socket.send(len_heather.encode())
		client_socket.send(str(float(width) * float(height) / 2).encode())


def upload(file_request, client_socket):
	"""
	the function check the validation of the request and make a file in the name that was asked
	in the request line
	:param file_request: any request that start with POST
	:param client_socket: the socket for the communication with the client
	:return: None
	"""
	if 'upload?file-name=' in file_request:
		data = b''
		file_properties = file_request.split('\r\n')
		file_start = file_properties[0].split(' ')
		start_part = file_start[1].split('=')
		file = 'webroot/uploads/' + start_part[1]
		for i in file_properties:
			if i.startswith("Content-Length:"):
				length_part = i.split(' ')
				data_len = length_part[1]
				break
			else:
				data_len = 0
		for i in range(int(data_len)):
			client_request = client_socket.recv(1)
			if client_request == '':
				break
			data += client_request
		try:
			with open(file, 'wb') as fd:  # open the file to write as binary file
				fd.write(data)
			client_socket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
		except Exception as err:
			print(err)
	else:
		client_socket.send(REDIRECTION_DICTIONARY[400].encode())


def image(image_name, client_socket):
	"""
	Show in the website the image that has the name that was in the request line
	:param image_name: name of image in the upload files
	:param client_socket: the socket for the communication with the client
	:return: None
	"""
	file_name = 'webroot/uploads/' + image_name
	try:
		with open(file_name, 'rb') as fd:
			data = fd.read()
		filename, file_extension = os.path.splitext(image_name)
		file_type = file_extension[1:]
		if file_type in TYPE_DICTIONARY.keys():
			type_header = TYPE_DICTIONARY[file_type]
			type_header = 'Content-Type: ' + type_header + '\r\n'
		len_header = 'Content-Length: ' + str(len(data)) + '\r\n\r\n'
		client_socket.send(REDIRECTION_DICTIONARY[200].encode())
		client_socket.send(type_header.encode())
		client_socket.send(len_header.encode())
		client_socket.send(data)
	except FileNotFoundError:
		client_socket.send("HTTP/1.1 404 NOT FOUND\r\n\r\n".encode())


if __name__ == "__main__":
	# Call the main handler function
	assert get_file_data("test.txt") == b'Hand Grenade of Antioch'
	assert validate_http_request("GET / HTTP/1.1") == (True, "")
	assert validate_http_request("GET  / HTTP/1.1") == (False, "")
	assert validate_http_request("GET /abcd HTTP/1.1") == (True, "abcd")
	assert validate_http_request("GET HTTP/1.1") == (False, "")
	main()
