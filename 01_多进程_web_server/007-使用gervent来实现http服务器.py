import socket 
import re
#import threading
import os
import gevent
from gevent import monkey

# 有耗时操作时需要
monkey.patch_all() # 将程序中用到的耗时操作的代码，换为gevent中自己实现的模块

def service_client(new_client):
	"""为这个客户端返回数据"""
	# 1.接收浏览器发送过来的请求，即http请求
	# GET / HTTP/1.1
	
	request = new_client.recv(1024).decode("utf-8")
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
		response = "HTTP/1.1 200 OK\r\n"
		response += "\r\n"
		new_client.send(response.encode("utf-8"))
		
		# 将response body发送给浏览器
		new_client.send(html_content)

	# 关闭套接字
	new_client.close()


def main():
	"用来完成整体的控制"
	# 1.创建套接字
	tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# 2.绑定
	tcp_server_socket.bind(("", 7890))

	# 3.变为监听套接字
	tcp_server_socket.listen(128)
	# 4.等待新用户链接
	while True:
		new_client, client_addr = tcp_server_socket.accept()

	# 5.为这个客户端服务
		gevent.spawn(service_client, new_client)

		# service_client(new_client)
		print("当前请求进程为%d"%os.getpid())
	tcp_server_socket.close()

if __name__ == "__main__":
	main()
