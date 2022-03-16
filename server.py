import socket
import os
from _thread import *
import pickle

host = '127.0.0.1'
port = 1233
ThreadCount = 0
Votes=[0,0,0,0,0]
Clients=[]
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)

def count_Votes(idx):
    
    Votes[int(idx)] += 1

def threaded_client(connection):
    global ThreadCount
    connection.send(str.encode('Welcome to the Server\n'))
    Clients.append(connection)
    print(Clients)
    while True:
        data = connection.recv(2048)
        idx = int(data.decode())
        if not data:
            break
        if idx < 5:
            count_Votes(idx)
        else:
            ThreadCount -= 1
        for i in range(len(Clients)):
            reply = pickle.dumps(Votes)
            Clients[i].send(reply)
            Clients[i].send(str(ThreadCount).encode())
        if ThreadCount == 0:
            print("done")

    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
ServerSocket.close()