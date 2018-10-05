# coding:utf-8
import socket
import re

def service_client(new_socket):
	'''为客户端返回数据'''
	# 1.接受请求
	request = new_socket.recv(1024).decode("utf-8")
	print(request)
	print("*"*20)
	request_lines = request.splitlines()
	print(">"*20)
	# print(request_lines[0])
	
	file_name = ""
	ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])
	if ret:
		file_name = ret.group(1)
		if file_name == "/":
			file_name = "/index.html"

	# 2.返回http格式的数据，给浏览器
	try:
		f = open("./html"+file_name, "rb")
	except:
		response = "HTTP/1.1 404 NOT FOUND\r\n"
		response += "\r\n" # 表示header内容结束
		response += "------file not found-------" # body内容
		new_socket.send(response.encode("utf-8"))

	else:
		html_content = f.read()
		f.close()
		# 2.1准备发送给浏览器的数据--header

		response = "HTTP/1.1 200 OK\r\n"
		response += "\r\n"
		

		# 2.2准备发送给浏览器的数据
		new_socket.send(response.encode('utf-8'))
		new_socket.send(html_content)
			
	new_socket.close()


def main():
	# 1.创建TCP套接字
	tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# 1.1 设置客户端套接字关闭，服务器释放
	tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# 2.绑定本机IP、port，传入数据以元组形式
	tcp_server_socket.bind(("", 7890))
	# 3.变为监听套接字
	tcp_server_socket.listen(128)
	
	while True:
		# 4.等待新客户端的链接，如果没有链接一直堵塞
		new_socket, client_addr = tcp_server_socket.accept()
		# 4.1 new_socket 保存客户端信息
		# 4.2 client_addr 保存客户端ip/port信息
		# print((new_socket,client_addr))
		
		# 5.为整个客户端提供服务
		service_client(new_socket)
	
	tcp_server_socket.close()

if  __name__ == "__main__":
	main()


