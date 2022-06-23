import socket
import threading
import pymongo
from pymongo import MongoClient
from concurrent.futures import thread
from http import client
from pickle import TRUE

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set()
clients_lock = threading.Lock()

myclient = MongoClient(
    "mongodb+srv://akhoa1107:anhkhoa123@cluster0.ns8gwdm.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]
collection = mydb["mydatabase"]


def receive(conn, prefix):
    conn.send(prefix.encode(FORMAT))
    return conn.recv(2048).decode(FORMAT)


def signupChecker(conn, username, password):
    if (len(username) < 5):
        return 0
    if (len(password) < 3):
        return 0
    for x in username:
        if not x.isnumeric() and not x.isalpha():
            return 0

    return 1


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        conn.send("Would you like signup or login (signup/login)?".encode(FORMAT))
        ans = conn.recv(2048).decode(FORMAT)
        if ans.lower() == 'signup':
            username = receive(conn, "Username: ")
            password = receive(conn, "Password: ")
            out = signupChecker(conn, username, password)
            if out == 1:
                conn.send("Sign up successfully".encode(FORMAT))
            else:
                conn.send("Invalid username or password".encode(FORMAT))

        if ans.lower() == 'login':
            username = receive(conn, "Username: ")
            password = receive(conn, "Password: ")
            results = collection.find_one({"username": username})

            if results != None and results["password"] == password:
                conn.send("Login successfully".encode(FORMAT))
                try:
                    connected = True
                    while connected:
                        msg = conn.recv(2048).decode(FORMAT)
                        if not msg:
                            break
                        if msg == DISCONNECT_MESSAGE:
                            connected = False
                        print(f"[{addr}] {msg}")
                        with clients_lock:
                            for c in clients:
                                c.sendall(f"[{addr}] {msg}".encode(FORMAT))
                finally:
                    with clients_lock:
                        clients.remove(conn)
                    conn.close()
                    return
            else:
                conn.send("Invalid username or password".encode(FORMAT))


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Server is starting...")
start()
