#!/bin/python3
import socket
import sys
import os

from encryption import *

serverName = '127.0.0.1' #'localhost'

def readFile(fileName):
    f = open(fileName, "r")
    contents = f.read()
    return contents

def recvAll(connectionSocket):
""" recves all content for a tcp connectionSocket, Just sends the length as plain asci
"""
        msg = connectionSocket.recv(2048).decode('ascii')
        pos = msg.find("\r\n\r\n")
        
        contents = msg[pos:]
        content_length = msg[:pos]

        recv_length =+ len(contents)
        # Get any remaining content from socket
        while(content_length > recv_length):
            msg = connectionSocket.recv(2048).decode('ascii')
            contents += msg[pos:]
            recv_length += len(msg)
        
        return contents

def Name():
    return input ("Please Enter Your name: ")

def serverIP():
    return input("Please enter server's IP Address: ")

    
#Create client socket that useing IPv4 and TCP protocols
def serverConnection():
    serverPort = 13000


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


def encrypt_username(connection, key, username):
    username_encrypted = encryptPublic(key, username)
    connection.send(username_encrypted)
    print("Client name sent to the server")




def server_handler():
    
    username = Name().lower()

    serverPublicKey = RSA.importkey(open("server_public.pem","rb").read())

    clientSocket = serverConnection()

    encrypt_username(clientSocket,serverPublicKey,username)

    sym_Key_encoded = clientSocket.recv(2048)

    try:
        clientPublicKey = RSA.importKey(open(username + "_public.pem","rb").read())
        clientPrivateKey = RSA.importKey(open(username + "_private.pem","rb").read())

        symKey = decryptPrivate(clientPrivateKey,sym_Key_encoded)

        print("Symmetric Key Received of the server")

        server_cipher = AES.new(symKey, AES.MODE_ECB)

        server_msg = clientSocket.recv(2048)

        server_msg = decryptSym(server_cipher, server_msg)

        fileName = input(server_msg)

        clientSocket.send(encryptSym(server_cipher, fileName))

        server_msg = clientSocket.recv(2048)

        server_msg = decryptSym(server_cipher, server_msg)

        print(server_msg)

        size_of_file = readFile(fileName)

        size_of_file = size_of_file + 16 - (size_of_file %16)

        clientSocket.send(encryptSym(server_cipher,str(size_of_file)))

        server_msg = clientSocket.recv(2048)
        server_msg = decryptSym(server_cipher, serve_msg)
        if (server_msg == "NO"):
            print("The file is too large. \n Terminating")

        else:
            contents_of_file = readFile(fileName)

            clientSocket.send(encryptSym(server_cipher, contents_of_file))

            print("The file size is OK. \n Sending file contents to server.\n The file is saved")
            clientSocket.close()

    except:

        error = sym_Key_encoded.decode()

        if error == "Invalid clientName":
            print("Invalid client name. \nTerminating")

        else:
            print(" error checking") #comment out later

            clientSocket.close()



#server_handler()
