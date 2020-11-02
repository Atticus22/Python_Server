#******************************************************************************
# Project           : Multi-threaded Server and Single-threaded Client
#
# Program name      : client.py
#
# Author            : Jhostin Nunez
#
# Date created      : 10/23/2020
#
# Purpose           : This is the client program that simulates multiple session
#                     when connected to a server.It also returns the following data:
#                       
#                     Running time - Time it took for one single request
#                     Total time - Time for all client requests to be finished
#                     Average time - Average time for each cleint request
#                     Command output - The output for each command 
#
# Revision History  : Date        Author          Revision
#                     10/22/2020  Jhostin Nunez   Finished fixing the IP adress 
#                                                 issue and input for the 
#                                                 commands have been implemented     
#
#******************************************************************************

import socket
import threading
from threading import Lock
import time
client_runtime = []
SERVER = 0

class ClientThread(threading.Thread):
    def __init__(self, outdata):
        threading.Thread.__init__(self)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.csocket = client
        mutex.acquire()
        self.csocket.connect((SERVER, PORT))

        start =  time.time()*1000
        print("\nclient connected")
        self.csocket.sendall(bytes(out_data, 'UTF-8'))

        if out_data == 'exit':
            self.csocket.close()
            return None

        print (self.csocket.recv(8192).decode())
        self.csocket.close()

        end = time.time()*1000

        print("running time: ",  round(end-start, 4), " ms")
        client_runtime.append(end - start)

        mutex.release()
        return None


# boolena values
flag_command = False
flag_ip = False
flag_port = False

# event loop
while(True):

    mutex = Lock()

    # available commands
    my_command_list = ["processes", "memory", "netstat", "users", "datetime",  "uptime", "exit"]

    print("\nEnter command:")
    print("\nprocesses | memory | netstat | users | datetime | uptime |exit")
    out_data = input()

    # checking if command is valid
    for i in range(0, len(my_command_list)):
        if(my_command_list[i] == out_data):
            print("\ncommand found")
            flag_command = True

    while(flag_command == False):
        print("\nthis command is not in list")
        print("Enter Command from list: ")
        print("\nprocesses | memory | netstat | users | datetime | uptime | exit")
        out_data = input()

    for i in range(0, len(my_command_list)):
        if(my_command_list[i] == out_data):
            flag_command = True


    if(out_data == "exit"):
        if SERVER == 0:
            break

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER, PORT))
        client.sendall(bytes(out_data, 'UTF-8'))
        break

    # validating IP address and PORT
    # change to your specs
    print("\nenter server IP address:")
    SERVER = input()

    if(SERVER == "127.0.0.1"):
        flag_ip = True

    while(flag_ip == False):
        print("\nWrong server IP Address")
        print("\nenter server IP address Again:")
        SERVER = input()
        if(SERVER == "127.0.0.1"):
            flag_ip = True

    print("\nEnter Port Number: ")
    PORT = int(input())

    if int(PORT) >= 1025 and int(PORT) <= 4998:
        flag_port = True

    while(flag_port == False):
        print("\nWrong Port Number")
        print("Enter Port Number Again: ")
        Port = int(input())
        if int(PORT) >= 1025 and int(Port) <= 4998:
            flag_port = True

    # getting required data
    print("\nEnter number of clients:")
    clientNum = int(input())

    threads = []

    # multiple threads
    for i in range(0, clientNum):
        newthread = ClientThread(out_data)
        threads.append(newthread)
        newthread.start()

    for x in threads:
        x.join()

    print("\nTotal running time: ", round(sum(client_runtime), 4), " ms")
    print("Avg running time: ", round(sum(client_runtime) /
          len(client_runtime), 4), " ms")

    client_runtime = []
