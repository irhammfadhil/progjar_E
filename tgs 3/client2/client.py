import os
import sys
import json
import socket

port = 3000

def checkArg(str):
    if len(str)==1:
        return {'cmd' : str[0].upper()}
    else:
        return {'cmd' : str[0].upper(), 'arg' : str[1]}

def get(str,s):
    js = checkArg(str)
    s.send(json.dumps(js))
    reply = json.loads(s.recv(1024))
    if ('err' in reply):
        print reply['err']
    else:
        print reply['action']
        with open(os.path.join('./', str[1]), 'wb') as f:
            while (True):       
                l = s.recv(1024)
                while (l):
                    f.write(l)
                    l = s.recv(1024)
                break
        print str[1]+' Success'    

def put(str, s):
    if (len(str)==1):
        print 'Syntax error'
        s.sendall(json.dumps({'cmd' : 'PUT','err' : 'Syntax error'}))
    else:
        filename = './' + str[1]
        if os.path.exists(filename):
            s.sendall(json.dumps({'cmd' : 'PUT','arg' : str[1]}))
            print 'Success'
            with open(filename, 'rb') as f:
                for line in f:
                    s.sendall(line)
            print str[1]+' Success'
        else:
            print 'File not found'
            s.sendall(json.dumps({'cmd' : 'PUT','err' : 'File not found'}))    

def rm(str,s):
    js = checkArg(str)
    s.send(json.dumps(js))
    reply = json.loads(s.recv(1024))   
    if('err' in reply):
        print 'File not found'
    else:
        print 'Success'

def ls(str,s):
    js = checkArg(str)
    s.send(json.dumps(js))
    rcvdData = s.recv(1024)
    rcvdData = json.loads(rcvdData)
    print "Server:",rcvdData['data']

def myserver():
    while True:
        s = socket.socket()
        try:
            s.connect(('127.0.0.1', port))
        except socket.error as err:
            print "Failed to connect, error %s" %(err)
            sys.exit()
    
        str = raw_input("Input Command, 'help' for help: ")
        str = str.split()    

        if(str[0].upper() == "LS"):
            ls(str,s)

        elif(str[0].upper() == "GET"):
            get(str,s)

        elif(str[0].upper() == "PUT"):
            put(str,s)

        elif(str[0].upper() == "RM"):
            rm(str,s)

        elif(str[0].upper() == "HELP"):
            js = checkArg(str)
            s.send(json.dumps(js))
            print "------------------------------------------------"
            print "Available command : ls, get, put, rm, quit, help"
            print "------------------------------------------------"

        elif(str[0].upper() == "QUIT"):
            js = checkArg(str)
            s.send(json.dumps(js))
            break

        else:
            js = checkArg(str)
            s.send(json.dumps(js))
            rcvdData = s.recv(1024)
            rcvdData = json.loads(rcvdData)
            print "Server:",rcvdData['data']

        s.close()

myserver()


