import socket
import re


def service_client(client_socket, recv_data):
	request_lines = recv_data.splitlines()
	# print(request_lines)
	ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])
	file_name = ""
	if ret:
		# print(ret, ret.group(1))
		file_name = ret.group(1)
		print(file_name)
		if file_name == "/":
			file_name = "/index.html" 

	try:
		file_name = "./html"+file_name

		f = open(file_name, "rb")
		print("-"*30)
	except Exception as e:
		
		response_body = "file not found"	
		response_header = "HTTP/1.1 404 NOT FOUND\r\n"
		response_header += "Content-Length:%d\r\n" % len(response_body)
		response_header += "\r\n"
		response = response_header+response_body

		client_socket.send(response.encode('utf-8'))
	else:
		print('读取页面内容')
		html_content = f.read()
		response_body = html_content
		print('读取完毕')
		f.close()
		response_header = "HTTP/1.1 200 OK\r\n"
		print('-------1-------')
		response_header += "Content-Length:%d\r\n" % len(response_body)
		print('-------2-------')
		response_header += "\r\n"
		print('-------333-----')
		response = response_header.encode('utf-8') + response_body
		print('-------4-------')
		client_socket.send(response)
		print('-------5-------')
		

def main():
	tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcp_server_socket.bind(('', 7890))
	tcp_server_socket.listen(128)
	tcp_server_socket.setblocking(False)

	client_socket_list = list()	

	while True:
		try:
			# time.sleep(0.5)
			new_client, client_addr = tcp_server_socket.accept()
		except Exception as e:
			#print("没有客户连入")
			# print(e)
			pass
		else:
			client_socket_list.append(new_client)
			new_client.setblocking(False)
		for client_socket in client_socket_list:
			# time.sleep(0.5)
			try:
				recv_data = client_socket.recv(1024).decode("utf-8")
			except:
				#print("客户端没有发送任何信息")
				pass
			else:
				if recv_data:
					print('收到客户发送消息', recv_data)
					service_client(client_socket, recv_data)
				else:
					client_socket.close()
					client_socket_list.remove(client_socket)
					
	tcp_server_socket.close()
				

if __name__ == "__main__":
	main()
