import socket
import time
import sys
import os

ip = ["127.0.0.1", "127.0.0.2", "127.0.0.3", "127.0.0.4"]
port = 9000
buf = 1024
file_name=["mrt.jpg", "balsam1.PNG", "singapore.jpg"]
#sock.bind((ip, port))
#sock.listen(1)
#conn, addr = sock.accept()

def send_file(filename, address, ports):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#print f
	f = filename
	size = os.stat(f).st_size
	sock.sendto(f, (address, ports))
	print "Sending %s ..." %f
	sent = 0
	f = open(f, "rb")
	data = f.read(buf)
	while (data):
		if(sock.sendto(data, (address, ports))):
			data = f.read(buf)
			sent+=1
			print 'Sent {} from {}'. format(sent, size)
			#time.sleep(0.02)
	sock.close()
	f.close()
	time.sleep(10)


for ip_address in ip:
	for i in range(len(file_name)):
		send_file(file_name[i], ip_address, port)