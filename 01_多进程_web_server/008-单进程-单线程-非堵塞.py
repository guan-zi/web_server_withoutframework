import socket
import time


tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcp_server_socket.setsockopt(socket.SOL_SOCK, socket.SO_REUSEADDR, 1)

tcp_server_socket.bind(("", 7890))
tcp_server_socket.listen(128)

tcp_server_socket.setblocking(False) #设置套接字为非堵塞方式

client_socket_list = list()

while True:
	try:
		new_socket, client_addr = tcp_server_socket.accept()

	except Exception as ret:
		print("-----没有新的客户端到来------")
	else:
		print("---只要没有异常，那么意味着来了一个新客户端---")
		new_socket.setblocking(False)
		client_socket_list.append(new_socket)

	for client_socket in client_socket_list:
		try:
			recv_data = client_socket.recv(1024)
		except Exception as ret:
			print(ret)
			print("--这个客户端没有发送数据过来--")
		else:
			print('---没有异常---')
			print(recv_data)
			if recv_data:
				print("--客户端数据发送过来了--")

			else:
				client_socket.close()
				client_socket_list.remove(client_socket)
				print('--客户端已关闭--')
			

