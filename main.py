import socket
import os
from _thread import *
from time import sleep

import pickle
import redis

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
redis_host = "0.0.0.0"
redis_port = 6379
Threadcount = 0

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))
    
print('Waiting for a connection')
ServerSocket.listen(5)

def threaded_client(connection):
    connection.send(str.encode('Welcome to the Server'))
    filename = connection.recv(2048)
    r = redis.StrictRedis(redis_host, redis_port)
    last_updated = -1
    try:
        while True:
            db_value = r.get(filename)
            if db_value is not None and type(db_value) != str :
                value = pickle.loads(db_value)
                if value['time'] != last_updated:
                    connection.sendall(str.encode(value['log']))
                    last_updated = value['time']
            sleep(0.5)           
    except Exception as e:
        print(str(e))
        connection.close()
        

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    Threadcount += 1
    print('Thread number: ' + str(Threadcount))

ServerSocket.close()
