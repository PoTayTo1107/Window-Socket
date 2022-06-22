from email import message
from http import client
import socket
import time

PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "26.183.40.49"
ADDR = (SERVER, PORT)


def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client


def send(client, msg):
    message = msg.encode(FORMAT)
    client.send(message)


def start():
    answer = input('Would you like to connect (yes/no)? ')
    if answer.lower() != 'yes':
        return
    
    connection = connect()
    while True:
        msg = input("Message (q for quit): ")
        
        if (msg == 'q'):
            break
        
        send(connection, msg)
        
    send(connection, DISCONNECT_MESSAGE)
    time.sleep(1)
    print('Disconnect')
    
start()
