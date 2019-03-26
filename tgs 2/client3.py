import socket
import select
import os

udp_ip = "127.0.0.3"
port = 9000
timeout = 3
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((udp_ip, port))
#sock.listen(10)

path = './fileclient3/'
if not os.path.exists(path):
	os.makedirs(path)

while True:
	data, addr = sock.recvfrom(1024)
	if data:
		print "File name:", data
		file_name = data.strip()
		print file_name
		name = os.path.splitext(file_name)[0]
		file_extension = os.path.splitext(file_name)[1]
		print file_extension
	filenamedest = name + 'copy3' + file_extension
	print filenamedest
	complete = os.path.join(path, filenamedest)
	f = open(complete, 'wb')

	
	while True:
		ready = select.select([sock], [], [], timeout)
		if ready[0]:
			data, addr = sock.recvfrom(1024)
			f.write(data)
		else:
			print "%s Finish!" % file_name
			f.close()
			#sock.close()
			break
	