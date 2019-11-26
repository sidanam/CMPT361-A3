#!/bin/python3
import socket
import sys
import os
from Crypto.Cipher import AES


port = 13000 #Associate port number to the server socket
serverSocket = False

serverPublicKeyFile=""# file path of the server public key
serverPrivateKeyFile=""
# client information
clients = {"client1":"./Client/",
               "client2":"./Client/",
               "client3":"./Client/"}

serverPublic='' # Server Private Key Cypher
serverPrivate=''# Server Public key Cypher

with open(serverPublicKeyFile, 'r') as keyfile:
    key = keyfile.read()
    serverPublic = AES.new(key, AES.MODE_ECB)

with open(serverPrivateKeyFile, 'r') as keyfile:
    key = keyfile.read()
    serverPrivate = AES.new(key, AES.MODE_ECB)



def clientHandler(connectionSocket):
    """" Interaction with an individual client
    @param connectionSocket - socket"""

    # TODO Recive client name
    connectionSocket.send("".encode('ascii'))

    # if there is a client with that name, generate and send AES key.
    # encript with that clients public key.
    #Server receives client message, decode it and convert it to upper case

    #  [Server side] After receiving the client name and decrypting it, the server checks whether this name is one of the known client folders’ names:

    
    clientName = connectionSocket.recv(2048)
    # dycrypt with server private key.

    if clientName in clients:
        
# - The server program generates a 256 AES key (called sym_key) and send it to the client encrypted with the corresponding client public key.
# - Then the server program prints on the server screen the following message “Connection Accepted and Symmetric Key Generated for client: [client_name]”

    else:#  If no,
        print(f"The received client:{clientName} is invalid (Connection Terminated)")
        connectionSocket.send("Invalid clientName".encode('ascii'))


    
    modifiedMessage = message.decode('ascii').upper()
        
    #Server sends the client the modified message
    print(modifiedMessage)
    connectionSocket.send(modifiedMessage.encode('ascii'))
    

# Connection Accepted and Symmetric Key Generated for client: [client_name]



try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print('Error in server socket creation:',e)
    sys.exit(1)
    
try:
    serverSocket.bind(('', port))
except socket.error as e:
    print('Error in server socket binding:',e)
    sys.exit(1)


print('The server is ready to accept connections')
#The server can only have one connection in its queue waiting for acceptance
serverSocket.listen(5)

# ------ Main Loop ------
while 1:
    try:
        # Server accepts client connection
        connectionSocket, addr = serverSocket.accept()
        print(addr,'   ',connectionSocket)
        pid = os.fork()
        
        # If it is a client process
        if  pid == 0:# This is the child Process of the 
            serverSocket.close()

            clientHandler(connectionSocket)
            connectionSocket.close()
            # Server send a message to the client
            
            os._exit(0)# exit the forked process
            
        #Parent doesn't need this connection
        connectionSocket.close()
        

    except socket.error as e:
        print('An error occured:',e)
        connectionSocket.close()
        serverSocket.close() 
        sys.exit(1)        
    except:
        print("Goodbye OR Unexpected error:", sys.exc_info())
        serverSocket.close()
        connectionSocket.close()
        sys.exit(0)
