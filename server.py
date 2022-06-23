import socket
import threading
import json
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


def receive(conn, prefix):
    conn.send(prefix.encode(FORMAT))
    return conn.recv(2048).decode(FORMAT)


def signupChecker(username, password):
    if (len(username) < 5):
        return 1
    if (len(password) < 3):
        return 2
    for x in username:
        if not x.isnumeric() and not x.isalpha():
            return 3
    data = openFile()
    for i in data['users']:
        if i['username'] == username:
            return 4
    return 0


def writeFile(username, password):
    user = {
        "username": username,
        "password": password,
    }
    with open('data.json', 'r') as file:
        data = json.load(file)
    data['users'].append(user)
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=2)


def openFile():
    with open('data.json') as file:
        data = json.load(file)
    file.close()
    return data


def signUpForm(conn):
    conn.send("Sign Up Form".encode(FORMAT))
    username = receive(conn, "Username: ")
    password = receive(conn, "Password: ")
    out = signupChecker(username, password)
    if out == 0:
        conn.send("Sign up successfully".encode(FORMAT))
        writeFile(username, password)
    if out == 1:
        conn.send("Username is too short".encode(FORMAT))
    if out == 2:
        conn.send("Password is too short".encode(FORMAT))
    if out == 3:
        conn.send("Username contains invalid character(s)".encode(FORMAT))
    if out == 4:
        conn.send("Username is already taken".encode(FORMAT))


def loginForm(conn):
    conn.send("Login Form".encode(FORMAT))
    username = receive(conn, "Username: ")
    password = receive(conn, "Password: ")
    data = openFile()
    for i in data['users']:
        if i['username'] == username and i['password'] == password:
            return 1, username
    return 0, username


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        conn.send('Would you like signup or login (signup/login)?'.encode(FORMAT))
        ans = conn.recv(2048).decode(FORMAT)
        if ans.lower() == 'signup':
            signUpForm(conn)

        if ans.lower() == 'login':
            login, username = loginForm(conn)
            if login == 1:
                conn.send('Login successfully'.encode(FORMAT))
                connected = True
                while connected:
                    msg = conn.recv(2048).decode(FORMAT)
                    if not msg:
                        break
                    if msg == DISCONNECT_MESSAGE:
                        connected = False
                    print(f"{username}: {msg}")
                conn.close()
                return
            conn.send('Invalid username or password'.encode(FORMAT))


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Server is starting...")
start()
