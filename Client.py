#!/bin/python3
import socket
import sys
import os


serverName = '127.0.0.1' #'localhost'
serverPort = 13000
    
    #Create client socket that useing IPv4 and TCP protocols 
try:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print('Error in client socket creation:',e)
    sys.exit(1)    
    
try:
    #Client connect with the server
    clientSocket.connect((serverName,serverPort))
        
    # Client receives a message and send it to the client
    message = clientSocket.recv(2048).decode('ascii')
        
    #Client send message to the server
    message = input(message).encode('ascii')
    clientSocket.send(message)
        
    # Client receives a message from the server and print it
    message = clientSocket.recv(2048)
    print(message.decode('ascii'))
        
    # Client terminate connection with the server
    clientSocket.close()
        
except socket.error as e:
    print('An error occured:',e)
    clientSocket.close()
    sys.exit(1)
