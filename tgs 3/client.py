import socket
import sys

if len(sys.argv) <= 2:
	print 'Usage: get/put (namafile/nama directory)'

#print sys.argv[0]
host = '127.0.0.1'
port = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
try:
	print('Terkoneksi dengan ' + host )
	command = sys.argv[1]
	inputan = sys.argv[2]
	s.sendall(command)
	set = s.recv(4096)
	if set == 'Begin':
		s.sendall(inputan)
		data = s.recv(4096)
		s.close()
		print 'Isi file ' + inputan + ':', repr(data)

except:
	print 'Error'