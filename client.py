import socket
import time
from email import message
from http import client

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


def form(connection):
    print(connection.recv(2048).decode(FORMAT))
    send(connection, input())
    print(connection.recv(2048).decode(FORMAT))
    send(connection, input())
    print(connection.recv(2048).decode(FORMAT))


def start():
    answer = input('Would you like to connect (yes/no)?\n')
    if answer.lower() != 'yes':
        return

    connection = connect()

    while True:
        print(connection.recv(2048).decode(FORMAT))
        rec = input()
        send(connection, rec)

        if rec.lower() == "signup":
            print('Signup Form')
            form(connection)

        if rec.lower() == "login":
            print('Login Form')
            form(connection)
            while True:
                msg = input("Message (q for quit): ")
                if (msg == 'q'):
                    break
                send(connection, msg)

            send(connection, DISCONNECT_MESSAGE)
            time.sleep(1)
            print('Disconnect')

start()
