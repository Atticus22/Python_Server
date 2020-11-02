#******************************************************************************
# Project           : Multi-threaded Server and Single-threaded Client
#
# Program name      : server.py
#
# Author            : Jhostin Nunez
#
# Date created      : 10/23/2020
#
# Purpose           : This is the server program that simulates a session
#                     when connected to a client.
#
# Revision History  : Date        Author          Revision
#                     10/22/2020  Jhostin Nunez   Finished fixing the IP adress 
#                                                 issue     
#
#******************************************************************************


import socket
import threading
import time
import datetime
import subprocess

#setting up variables
LOCALHOST = socket.gethostname() 
PORT = 2250
flag_ip = False
flag_port=False
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#input validation
print("enter IP address:")
Ip = input()

if (Ip == "127.0.0.1"):
    flag_ip = True

while (flag_ip == False):
    print("Wrong IP Address")
    print("enter IP address Again:")
    Ip = input()
    if (Ip == "127.0.0.1"):
        flag_ip = True


print("\nEnter Port Number: ")
Port = int(input())

if int(Port) >= 1025 and int(Port) <= 4998:
    flag_port = True

while (flag_port == False):
    print("\nWrong Port Number")
    print("Enter Port Number Again: ")
    Port = int(input())
    if int(Port) >= 1025 and int(Port) <= 4998:
        flag_port = True

server.bind((Ip, Port))

print("\nServer started")
print("Waiting for client(s) request.. \n")

clientReqs = []
opr = ""

#event loop
while True:
    server.listen()
    newsock = server.accept()[0]
    print("client connected from server side")

    clientReqs.append(newsock)

    for clientsock in clientReqs:
        data = clientsock.recv(1024)
        opr = data.decode()

        if opr == "exit":
            print ("\nClient disconnected...")
            server.close()
            break
            

        elif opr == "datetime":
            timestamp = datetime.datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p")
            clientsock.send(timestamp.encode())
            
        
        elif opr == "uptime":
            res = subprocess.check_output('uptime',shell=True)
            clientsock.send(res)
        
        elif opr == "memory":
            res = subprocess.check_output('free -h',shell=True)
            clientsock.send(res)
           
        elif opr == "netstat":
            res = subprocess.check_output('netstat',shell=True)
            clientsock.send(res)

        elif opr == "users":
            res = subprocess.check_output('w',shell=True)
            clientsock.send(res)
        
        elif opr == "processes":
            res = subprocess.check_output('ps',shell=True)
            clientsock.send(res)

        clientsock.close()
        clientReqs.pop(0)

    if opr == "exit":
        break