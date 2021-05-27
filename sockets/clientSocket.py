import sys

import socket

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

if len(sys.argv) < 2:
    ClientSocket.close()    
else:
    print('Waiting for connection')
    try:
        ClientSocket.connect((host, port))
    except socket.error as e:
        print(str(e))

    Response = ClientSocket.recv(1024)
    while True:
        ClientSocket.send(str.encode(sys.argv[1]))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))

    ClientSocket.close()