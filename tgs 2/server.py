import socket
import time
import sys
import os

ip = "127.0.0.1"
port = 9000
buf = 1024
file_name=["balsam1.PNG", "singapore.jpg"]
#sock.bind((ip, port))
#sock.listen(1)
#conn, addr = sock.accept()
def send_file(filename):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#print f
	f = filename
	size = os.stat(f).st_size
	sock.sendto(f, (ip, port))
	print "Sending %s ..." %f
	sent = 0
	f = open(f, "rb")
	data = f.read(buf)
	while (data):
		if(sock.sendto(data, (ip, port))):
			data = f.read(buf)
			sent+=1
			print 'Sent {} from {}'. format(sent, size)
			#time.sleep(0.02)
	sock.close()
	f.close()
	time.sleep(10)

for i in range(len(file_name)):
	send_file(file_name[i])
