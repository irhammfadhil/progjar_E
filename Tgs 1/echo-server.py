import sys
import socket

#tcp-ip socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_addr = ('localhost', 1234)

print >>sys.stderr, 'Starting up on %s on port %s' % server_addr
#bind
sock.bind(server_addr)

sock.listen(5)

while True:
	print >>sys.stderr, 'Waiting for a connection'
	conn, client_addr = sock.accept()
	print >>sys.stderr, 'Receiving connection from ', client_addr 
	while True:
		data=conn.recv(32)
		print >>sys.stderr, 'received "%s"' % data
		if data:
			conn.sendall(data)
		else:
			print 'No more data'
			break
	conn.close()