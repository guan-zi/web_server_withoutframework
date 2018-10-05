import socket 
import re


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
		# print("*"*50, file_name)
		if file_name == '/':
			file_name = "/index.html"

	try:
		# print("<"*20,file_name)
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
		# 在header 中增加Content-Length，是服务器告诉请求的客户端，响应数据有多长，接收完就不再加载，如无本行数据请求会一直加
		response_header += "\r\n"

		response = response_header.encode("utf-8")+response_body
		new_client.send(response)
		
		# 将response body发送给浏览器
		# new_client.send(html_content)

	# 长链接不需要关闭套接字
	# new_client.close()


def main():
	"用来完成整体的控制"
	# 1.创建套接字
	tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# 主进程退出后，释放端口
	# 2.绑定
	tcp_server_socket.bind(("", 7890))

	# 3.变为监听套接字
	tcp_server_socket.listen(128)
	tcp_server_socket.setblocking(False) # 将套接字设为非堵塞

	client_socket_list = list()
	# 4.等待新用户链接
	while True:
		try:
			new_client, client_addr = tcp_server_socket.accept()
		except Exception as ret:
			pass #没有客户端连入，遍历再接收
		else:
			new_client.setblocking(False) # 将连入的客户端套接字设为非堵塞
			client_socket_list.append(new_client)
			
		for client_socket in client_socket_list:# 轮询保存的客户端套接字列表，是否收到请求
			try:
				recv_data = client_socket.recv(1024).decode('utf-8')# recv 必须有参数，不然这里也会发生异常
			except Exception as ret:
				pass # 如果没有客户端连入，pass遍历下一个客户端
			else:
				if recv_data: # 收到请求，请求非空调用请求处理程序
					service_client(new_client, recv_data)
				else:
					client_socket.close()
					client_socket_list.remove(client_socket)

	# 5.为这个客户端服务

		# service_client(new_client)
		# print("当前请求进程为%d"%os.getpid())
	tcp_server_socket.close()


if __name__ == "__main__":
	main()
