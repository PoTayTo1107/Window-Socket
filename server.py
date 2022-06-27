import socket
import time
import os
import json
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def send(conn, msg):
    conn.send(msg.encode(FORMAT))


def receive(conn):
    return conn.recv(2048).decode(FORMAT)


def clscr():
    os.system('cls')


def signupChecker(username, password):
    if (len(username) < 5):
        return "1"
    if (len(password) < 3):
        return "2"
    for x in username:
        if not x.isnumeric() and not x.isalpha():
            return "3"
    data = openFile("users")
    for i in data:
        if i['username'] == username:
            return "4"
    return "0"


def writeFile(username, password):
    user = {
        "username": username,
        "password": password,
    }
    with open("users.json", "r") as file:
        data = json.load(file)
    data.append(user)
    with open("users.json", "w") as file:
        json.dump(data, file, indent=2)


def openFile(str):
    with open(f"{str}.json") as file:
        data = json.load(file)
    file.close()
    return data


def signupExe(conn, username, password):
    out = signupChecker(username, password)
    send(conn, out)
    if out == "0":
        writeFile(username, password)


def loginForm(conn):
    send(conn, "Login Form\n")
    username = receive(conn)
    password = receive(conn)
    data = openFile("users")
    for i in data:
        if i['username'] == username and i['password'] == password:
            return 1, username
    return 0, username


def sendFuncList(conn):
    send(conn, "Functions list\n1. Add new note\n2. Show all notes\nAny other key to exit\n")


def writeNote(content, datatype, username):
    with open("data.json", "r") as file:
        data = json.load(file)
    for i in data:
        if str(i) == username:
            data[f'{username}'][f'{datatype}'].append(content)
            with open("data.json", "w") as file:
                json.dump(data, file, indent=2)
            return
    data[f'{username}'] = {}
    data[f'{username}']['notes'] = []
    data[f'{username}']['imgs'] = []
    data[f'{username}']['files'] = []
    data[f'{username}'][f'{datatype}'].append(content)
    with open("data.json", "w") as file:
        json.dump(data, file, indent=2)


def addNote(conn, datatype, username):
    note = receive(conn, "Enter new note:")
    writeNote(note, datatype, username)
    send(conn, "Add new note successfuly")


def showNote(conn, username):
    data = openFile("data")
    if username in data:
        if len(data[f'{username}']['notes']) == 0:
            send(conn, "EMPTY")
        else:
            for i in data[f'{username}']['notes']:
                send(conn, i + '\n')


def handle_client(conn, addr):
    list = receive(conn)
    list = eval(list)
    print(list)
    if list[0] == "Sign up":
        signupExe(conn, list[1], list[2])
    elif list[0] == "Log in":
        login, username = loginForm(conn)
        if login == 1:
            send(conn, "Login successfully")
            print(f"[NEW CONNECTION] {username} connected.")
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
            while True:
                sendFuncList(conn)
                func = receive(conn)
                if func == "1":
                    addNote(conn, "notes", username)
                    time.sleep(1)
                elif func == "2":
                    showNote(conn, username)
                    time.sleep(1)
                else:
                    conn.close()
                    print(f"[DISCONNECTION] {username} disconnected.")
                    print(
                        f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
                    return
        else:
            send(conn, "Invalid username or password")


def start():
    clscr()
    server.listen()
    print("[STARTING] Server is starting...")
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


start()
