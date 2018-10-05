import socket 
import re
import select


def service_client(new_client, request):
	"""为这个客户端返回数据"""
	# 1.接收浏览器发送过来的请求，即http请求
	# GET / HTTP/1.1
	
	#request = new_client.recv(1024).decode("utf-8")
	print(request)
	
	request_lines = request.splitlines()
	print(">"*20)
	print(request_lines)
	
	file_name = ''
	
	ret = re.match(r'[^/]+(/[^ ]*)', request_lines[0])
	if ret:
		file_name = ret.group(1)
		print("*"*50, file_name)
		if file_name == '/':
			file_name = "/index.html"

	try:
		print("<"*20,file_name)
		f = open('./html'+file_name, "rb")
		# 打开匹配到的页面，如果未匹配到，执行except语句
	except:
		response = "HTTP/1.1 404 NOT FOUND\r\n"
		response += "\r\n"
		response += 'file not found'.center(50, '-')
		new_client.send(response.encode('utf-8'))
	else:
		html_content = f.read()
		# 能够打开匹配文件，读出文件内容
		f.close()
		# 2.1 准备发送给浏览器的数据--header
		response_body = html_content
		response_header = "HTTP/1.1 200 OK\r\n"
		response_header += "Content-Length:%d\r\n"%len(response_body)
		response_header += "\r\n" # 表示header内容结束

		response = response_header.encode("utf-8")+response_body
		new_client.send(response)
		
		# 将response body发送给浏览器
		# new_client.send(html_content)

	# 关闭套接字
	# new_client.close() # 长链接不需要关闭套接字


def main():
	"用来完成整体的控制"
	# 1.创建套接字
	tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# 2.绑定
	tcp_server_socket.bind(("", 7890))

	# 3.变为监听套接字
	tcp_server_socket.listen(128)
	tcp_server_socket.setblocking(False) # 将套接字设为非堵塞

	epl = select.epoll()
	# 创建一个epoll对象
	
	epl.register(tcp_server_socket.fileno(), select.EPOLLIN)
	# 将监听套接字对应的fd注册到epoll中，epl.register接收服务器‘套接字文件句柄’和‘事件类型’
	# select.EPOLLIN可写， select.EPOLLOUT可写， select.EPOLLERR错误， select.EPOLLHUP客户端断开类型
	fd_event_dict = dict()	

	# 4.等待新用户链接
	while True:
		fd_event_list = epl.poll()
		# 默认会堵塞，直到os检测到数据到来通过事件通知方式，告诉这个程序，此时才会解堵塞
		#[(fd, event),(套接字对应的文件描述符，这个文件描述符到底是什么事件，例如可以调用recv接收等)]
		for fd, event in fd_event_list:
			#等待新客户端的链接
			if fd == tcp_server_socket.fileno():
				new_socket, client_socket = tcp_server_socket.accept()

				epl.register(new_socket.fileno(), select.EPOLLIN) # 向列表中添加套接字句柄和事件类型

				fd_event_dict[new_socket.fileno()] = new_socket # 向列表字典中添加套接字文件句柄

			elif event == select.EPOLLIN: # 判断已经有链接的客户端是否有数据发送过来
				recv_data = fd_event_dict[fd].recv(1024).decode('utf-8')

				if recv_data: # 收到的请求数据非空，调用服务接口程序
					service_client(fd_event_dict[fd], recv_data)	
				else: # 受到的请求为空说明，客户端已经要挥手关闭，所以服务器客户套接字关闭
					fd_event_dict[fd].close()
					epl.unregister(fd) # 删除注册列表中的套接文件句柄
						
					del fd_event_dict[fd] # 删除文件句柄字典中的客户端套接字

	tcp_server_socket.close()


if __name__ == "__main__":
	main()


