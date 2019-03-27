import os
import sys
import glob
import json
import socket

def checkArg(cmd, data):
    return {'cmd' : cmd, 'data' : data}

try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Socket successfully created"
except socket.error as err:
    print "socket creation failed with error %s" %(err)
    sys.exit()

port = 3000

s.bind(('', port))
print "socket binded to %s" %(port) 

def ls(c,data):
    if ('arg' not in rcvdData):
        files = glob.glob('*')
    else:
        files = os.listdir('.')

    for name in files:
        data = data + name + '   '
    data = checkArg('LS',data)
    c.sendall(json.dumps(data))

def get(c,data):
    if ('arg' not in rcvdData):
        c.sendall(json.dumps({'cmd' : 'GET','err' : 'syntax error'}))
    else:
        filename = './' + rcvdData['arg']
        if os.path.exists(filename):
            c.sendall(json.dumps({'cmd' : 'GET', 'action': 'Success'}))
            with open(filename, 'rb') as f:
                for line in f:
                    c.sendall(line)
        else:
            c.sendall(json.dumps({'cmd' : 'GET','err' : 'File not found'}))

def put(c,data):
    if ('err' in rcvdData):
        print rcvdData['err']
    else:
        filename = rcvdData['arg']
        with open(os.path.join('./', filename), 'wb') as f:
            while (True):       
                l = c.recv(1024)
                while (l):
                    f.write(l)
                    l = c.recv(1024)
                break    

def rm(c,data):
    if ('arg' not in rcvdData):
        c.sendall(json.dumps({'cmd' : 'RM','err' : 'syntax error'}))
    else:
        filename = './' + rcvdData['arg']
        if os.path.exists(filename):
            c.sendall(json.dumps({'cmd' : 'RM', 'action': 'Success'}))
            os.remove(filename)
        else:
            c.sendall(json.dumps({'cmd' : 'RM','err' : 'File not found'}))       

s.listen(5)

while True:
    c, addr = s.accept()
    data = ""
    rcvdData = c.recv(1024)
    print "Client:",rcvdData
    rcvdData = json.loads(rcvdData)
    if (rcvdData['cmd'] == 'LS'):
        ls(c,data)

    elif(rcvdData['cmd'] == 'GET'):
        get(c,data)

    elif(rcvdData['cmd'] == 'PUT'):
        put(c,data)

    elif(rcvdData['cmd'] == 'RM'):
        rm(c,data)
        
    elif(rcvdData['cmd'] == 'HELP'):
        continue

    elif(rcvdData['cmd'] == 'QUIT'):
        break

    else:
        c.sendall(json.dumps({'cmd' : 'QUIT','data' : 'Unknown Command!'}))

    c.close()

s.close()