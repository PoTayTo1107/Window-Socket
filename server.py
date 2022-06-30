import io
import socket
import time
import os
import json
import threading
import base64

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


def loginExe(username, password):
    login = openFile("users")
    for i in login:
        if i['username'] == username and i['password'] == password:
            return "0"
    return "1"


def addUser(username):
    with open("userdata/data.json", "r") as file:
        userdata = json.load(file)
    if username not in userdata:
        userdata[username] = []
    with open("userdata/data.json", "w") as file:
        json.dump(userdata, file, indent=2)


def writeDataFile(conn, username, msg_list):
    with open("userdata/data.json", "r") as file:
        data = json.load(file)
    if msg_list[1] == 'Txt':
        dataToAdd = {
            "type": msg_list[1],
            "title": msg_list[2],
            "content": msg_list[3]
        }
    elif msg_list[1] == 'Image':
        image_path = f'userdata/{username}/imgs'
        try:
            os.makedirs(image_path)
        except FileExistsError:
            pass
        content = f'{image_path}/{msg_list[2]}'
        dataToAdd = {
            "type": msg_list[1],
            "title": msg_list[2],
            "content": content
        }
        image = open(content, "wb")
        image_chunk = conn.recv(4096000)
        image.write(image_chunk)
        image.close()
    elif msg_list[1] == 'File':
        file_path = f'userdata/{username}/files'
        try:
            os.makedirs(file_path)
        except FileExistsError:
            pass
        content = f'{file_path}/{msg_list[2]}'
        dataToAdd = {
            "type": msg_list[1],
            "title": msg_list[2],
            "content": content
        }
        file = open(content, "wb")
        file_chunk = conn.recv(4096000)
        file.write(file_chunk)
        file.close()
    data[username].append(dataToAdd)
    with open("userdata/data.json", "w") as file:
        json.dump(data, file, indent=2)


def sendData(conn):
    with open("userdata/data.json", "r") as file:
        data = json.load(file)
        if data != {}:
            send(conn, str(data))


def handle_client(conn, addr):
    while True:
        list = receive(conn)
        list = eval(list)
        if list[0] == "Sign up":
            signupExe(conn, list[1], list[2])
        elif list[0] == "Log in":
            out = loginExe(list[1], list[2])
            send(conn, out)
            if out == "0":
                print(f"[NEW CONNECTION] {list[1]} connected.")
                addUser(list[1])
                sendData(conn)
                while True:
                    msg_list = receive(conn)
                    msg_list = eval(msg_list)
                    if msg_list[0] == DISCONNECT_MESSAGE:
                        print(f"[DISCONNECTION] {list[1]} disconnected.")
                        conn.close()
                        return
                    elif msg_list[0] == "Add":
                        writeDataFile(conn, list[1], msg_list)
                        sendData(conn)
                    elif msg_list[0] == "Show":
                        img = open(msg_list[1], "rb")
                        data = base64.b64encode(img.read())
                        conn.send(data)

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
