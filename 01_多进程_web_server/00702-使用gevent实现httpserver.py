import socket
import gevent
from gevent import monkey
import re

monkey.patch_all()

def service_client(new_socket):
	request = new_socket.recv(1024).decode('utf-8')
	requestlines = request.splitlines()
	#print(">"*20, requestlines)
	filename = ''
	ret = re.match(r"[^/]+(/[^ ]*)", requestlines[0])
	#print("<"*20, ret.group(1))
	if ret:
		filename = ret.group(1)
		#print("-"*20, filename)
		if filename == '/':
			filename = "/index.html"
	
	try:
		f = open("./html"+filename, "rb")
	except:
		response = "HTTP/1.1 404 NOT FOUND\r\n"
		response += "\r\n"
		response += "----file not found-----"
		new_socket.send(response.encode('utf-8'))
	else:
		response_body = f.read()
		f.close()
		response_header = "HTTP/1.1 200 OK\r\n"
		response_header += "Content-Length:%d\r\n"%len(response_body)
		response_header += "\r\n"
		response = response_header.encode('utf-8')+response_body
		new_socket.send(response)
	new_socket.close()
	


def main():
	tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcp_server_socket.bind(("", 7890))
	
	# tcp_server_socket.setblocking(False)
	tcp_server_socket.listen(128)

	while True:
		new_socket, client_addr = tcp_server_socket.accept()
		gevent.spawn(service_client, new_socket)

	tcp_server_socket.close()
			




if __name__ == "__main__":
	main()
