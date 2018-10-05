import socket


def service_client(new_socket):
	'''为客户端返回数据'''
	# 接受请求
	request = new_socket.recv(1024)
	print(request)
	
	# 返回http格式的数据，给浏览器
	# 准备发送给浏览器的数据--header
	response = "HTTP/1.1 200 OK\r\n"
	response += "\r\n"
	
	# 准备发送给浏览器的数据
	response += "welcome"
	new_socket.send(response.encode('utf-8'))
	
	new_socket.close()


def main():
	# 创建TCP套接字
	tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# 绑定本机IP、port，传入数据以元组形式
	tcp_server_socket.bind(("", 7890))
	# 监听
	tcp_server_socket.listen(128)
	
	while True:
		# 等待新客户端的链接，如果没有链接一直堵塞
		new_socket, client_addr = tcp_server_socket.accept()
		
		# 为整个客户端提供服务
		service_client(new_socket)
	
	tcp_server_socket.close()

if  __name__ == "__main__":
	main()


