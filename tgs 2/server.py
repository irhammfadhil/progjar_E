import socket
import time
import sys

ip = "127.0.0.1"
port = 9000
buf = 1024
file_name="singapore.jpg.PNG"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(file_name, (ip, port))
print "Sending %s ..." %file_name

f = open(file_name, "rb")
data = f.read(buf)
while (data):
	if(sock.sendto(data, (ip, port))):
		data = f.read(buf)
		time.sleep(0.02)

sock.close()
f.close()