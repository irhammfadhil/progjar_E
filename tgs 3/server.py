import socket
import os
import sys
from threading import Thread

path = os.getcwd()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '127.0.0.1'
port= 5000
s.bind((ip, port))
s.listen(5)
#conn, addr = None

print "Waiting for client..."

def init():
	#global conn, addr
	while True:
		conn, addr = s.accept()
		print addr
		data = conn.recv(4096)
		if str(data) == 'get' or str(data) == 'put':
			thread = Thread(target=process)
			thread.start()
			conn.sendto("Begin", addr)


def process(ip, port):
	global conn, addr
	addr = (ip, port)
	while 1:
		data = conn.recv(4096)
		print data
		if not data:
			break
		c = listFiles(data)
		conn.sendall(c)
		conn.close()

def listFiles(input):
	global path
	#print input
	#path = os.getcwd()
	#print 'List files and directories in ' + path + ':'
	files = os.listdir(path)
	for file in files:
		#print file
		if os.path.isdir(file):
			#print file + ' is a directory'
			if input == file:
				#print file
				newdir = path + "\\" + input
				#print newdir
				os.chdir(newdir)
				path = os.getcwd()
				#print 'Current path after changing directory: ' + path
				return 'folder'
				break
		elif os.path.isfile(file):
			#print file + ' is a file'
			if input == file:
				#print file
				with open(input, 'r') as fin:
					#print 'Isi file ' + input + ' :'
					e = fin.read()
					fin.close()
					return e
				break

'''
print ('Waiting for client...')
s.listen(5)
conn, addr = s.accept()
while 1:
	data = conn.recv(4096)
	print data
	if not data:
		break
	c = listFiles(data)
	if c != 'folder':
		conn.sendall(c)
conn.close()
'''

while True:
	init()