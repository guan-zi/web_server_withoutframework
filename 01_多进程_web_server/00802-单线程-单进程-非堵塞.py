import socket
import time


tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_server_socket.bind(('', 7890))
tcp_server_socket.listen(128)
tcp_server_socket.setblocking(False)
client_socket_list = list()

while True:
	try:
		time.sleep(0.5)
		new_socket, client_addr = tcp_server_socket.accept()
	except Exception as e:
		print("没有客户端连入")
		
	else:
		print("没有异常")
		new_socket.setblocking(False)
		client_socket_list.append(new_socket)

	for client_socket in client_socket_list:
		try:
			time.sleep(0.5)
			recv_data = client_socket.recv(1024)
		except Exception as e:
			print("客户端没有发来数据")
		else:
			if recv_data:
				print("客户端请求为%s"%recv_data.decode("utf-8"))
			else:
				client_socket.close()
				client_socket_list.remove(client_socket)
				print("客户端已关闭")
