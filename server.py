import socket
import time
import os
import json
import threading
import shutil

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


def openFile(str):
    with open(f"{str}.json") as file:
        data = json.load(file)
    file.close()
    return data


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


def signupExe(conn, username, password):
    out = signupChecker(username, password)
    send(conn, out)
    if out == "0":
        writeFile(username, password)


def loginExe(conn, username, password):
    data = openFile("users")
    for i in data:
        if i['username'] == username and i['password'] == password:
            return "0"
    return "1"


def writeDataFile(conn, username, msg_list):
    with open("userdata/data.json", "r") as file:
        data = json.load(file)
    if username not in data:
        data[username] = {}
        data[username]['title'] = []
        data[username]['note'] = []
        data[username]['img'] = []
        data[username]['file'] = []

    if msg_list[0] == 'note':
        data[username]['title'].append(msg_list[1])
        data[username]['note'].append(msg_list[2])
    elif msg_list[0] == 'img':
        path = f'userdata/imgs/{msg_list[1]}'
        file = open(path, "wb")
        image_chunk = conn.recv(4096000)
        file.write(image_chunk)
        data[username]['img'].append(path)
        file.close()
    elif msg_list[0] == 'file':
        data[username]['file'].append(msg_list[1])
    with open("userdata/data.json", "w") as file:
        json.dump(data, file, indent=2)


def showData(conn, username, msg_list):
    with open("userdata/data.json", "r") as file:
        data = json.load(file)
    if username in data:
        if len(data[username][msg_list[1]]) == 0:
            send(conn, "!ERROR")
        elif data[username][msg_list[1]] == 'note':
            send(conn, str(data[username]['title']))
            send(conn, str(data[username]['note']))
        elif data[username][msg_list[1]] == 'img':
            send(conn, str(data[username]['img']))
        elif data[username][msg_list[1]] == 'file':
            send(conn, str(data[username]['file']))


def deleteData(username, msg_list):
    pass


def handle_client(conn, addr):
    while True:
        list = receive(conn)
        list = eval(list)
        if list[0] == "Sign up":
            signupExe(conn, list[1], list[2])
        elif list[0] == "Log in":
            out = loginExe(conn, list[1], list[2])
            send(conn, out)
            if out == "0":
                print(f"[NEW CONNECTION] {list[1]} connected.")
                while True:
                    msg_list = receive(conn)
                    msg_list = eval(msg_list)
                    if msg_list[0] == DISCONNECT_MESSAGE:
                        print(f"[DISCONNECTION] {list[1]} disconnected.")
                        conn.close()
                        return
                    elif msg_list[0] == "Show":
                        showData(conn, list[1], msg_list)
                    elif msg_list[0] == "Delete":
                        deleteData(list[1], msg_list)
                    else:
                        writeDataFile(conn, list[1], msg_list)

        else:
            conn.close()
            break


def start():
    os.system('cls')
    server.listen()
    print("[STARTING] Server is starting...")
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


start()
