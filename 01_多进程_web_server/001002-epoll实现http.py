import socket
import re
import select
import sys


def service_client(client_socket, request):
	request_lines = request.splitlines()
	ret = re.match(r'[^/]+(/[^ ]*)', request_lines[0])
	file_name = ''
	if ret:
		file_name = ret.group(1)
		if file_name == "/":
			file_name = "/index.html"
	try:
		f = open("./html"+file_name, "rb")
	except:
		response_body = "file not found"
		response_header = "HTTP/1.1 404 NOT FOUND\r\n"
		response_header += "Content-Length:%d\r\n"%len(response_body)
		response_header += '\r\n'
		response = response_header+response_body
		client_socket.send(response.encode('utf-8'))
	else:
		response_body = f.read()
		f.close()
		response_header = "HTTP/1.1 200 OK\r\n"
		response_header += "Content-Length:%d\r\n"%len(response_body)
		response_header += '\r\n'
		response = response_header.encode('utf-8')+response_body
		client_socket.send(response)
		


def main():
	#if len(sys.argv) < 2:
	#	print("输入错误")
	tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcp_server_socket.bind(("", 7890))
	tcp_server_socket.listen(128)
	tcp_server_socket.setblocking(False)
	epl = select.epoll()
	epl.register(tcp_server_socket.fileno(), select.EPOLLIN)
	fd_event_dict = dict()
	while True:
		fd_event_list = epl.poll() # 默认会堵塞，直到os检测到数据到
		print([fd for fd, event in fd_event_list])
		for fd , event in fd_event_list:
			print(fd)
			print('----收到事件通知，轮询注册表----')
			if fd == tcp_server_socket.fileno(): # 如果服务器文件句柄收到时间通知，调用接收用户客户端
				new_client_socket, client_addr = tcp_server_socket.accept()
				epl.register(new_client_socket.fileno(), select.EPOLLIN)
				fd_event_dict[new_client_socket.fileno()] = new_client_socket
				print("---有心客户到来----")
			elif event == select.EPOLLIN:
				recv_data = fd_event_dict[fd].recv(1024).decode('utf-8')
				if recv_data:
					service_client(fd_event_dict[fd], recv_data)
					print(fd,"--客户有新请求---")
				else:
					fd_event_dict[fd].close()
					epl.unregister(fd_event_dict[fd])
					del fd_event_dict[fd]
					print(fd,'--客户离开---')
	tcp_server_socket.close()

if __name__ == "__main__":
	main()
