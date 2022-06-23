import socket
import time
import tkinter
import tkinter.scrolledtext
import threading
from tkinter import simpledialog
from email import message
from http import client

from server import receive

PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "26.183.40.49"
ADDR = (SERVER, PORT)


# def gui_loop(connection):
#     connection.win = tkinter.tk()
#     connection.win.configure(bg="lightgray")

#     connection.chat_label = tkinter.Label(
#         connection.win, text='Chat: ', bg="lightgray")
#     connection.chat_label.config(state='disabled')
#     connection.chat_label.pack(padx=20, pady=5)

#     connection.text_area = tkinter.scrolledtext.ScrolledText(connection.win)
#     connection.text_area.config(font=("Arial", 12))
#     connection.text_area.pack(padx=20, pady=5)

#     connection.msg_label = tkinter.Label(
#         connection.win, text='Message: ', bg="lightgray")
#     connection.msg_label.config(state='disabled')
#     connection.msg_label.pack(padx=20, pady=5)

#     connection.input_area = tkinter.Text(connection.win, height=3)
#     connection.input_area.pack(padx=20, pady=5)

#     connection.send_button = tkinter.Button(
#         connection.win, text='Send', command=connection.write)
#     connection.send_button.config(font=("Arial", 12))
#     connection.send_button.pack(padx=20, pady=5)

#     connection.gui_done = True

#     connection.win.protocol("WM_DELETE_WINDOW", connection.stop)

#     connection.win.mainloop()


# def write(connection):
#     message = f"{connection.nickname}: {connection.input_area.get('1.0','end')}"
#     send(connection, message)
#     connection.input_area.delete()


# def stop(connection):
#     connection.running = False
#     connection.win.destroy()
#     connection.sock.close()
#     exit(0)


# def receiveGui(connection):
#     pass


# def gui(connection):
#     msg = tkinter.tk()
#     msg.withdraw()

#     connection.nickname = simpledialog.askstring(
#         "Nickname", "Please choose nickname", parent=msg)

#     connection.gui_done = False
#     connection.running = True

#     gui_thread = threading.Thread(target=connection.gui_loop)
#     receive_thread = threading.Thread(target=connection.receiveGui)


def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client


def send(client, msg):
    message = msg.encode(FORMAT)
    client.send(message)


def recvPrint(connection):
    print(connection.recv(2048).decode(FORMAT))


def form(connection):
    recvPrint(connection)
    recvPrint(connection)
    send(connection, input())
    recvPrint(connection)
    send(connection, input())


def start():
    answer = input('Would you like to connect (yes/no)?\n')
    if answer.lower() != 'yes':
        return

    connection = connect()

    while True:
        recvPrint(connection)
        rec = input()
        send(connection, rec)

        if rec.lower() == 'signup':
            form(connection)
            recvPrint(connection)

        if rec.lower() == 'login':
            form(connection)
            noti = connection.recv(2048).decode(FORMAT)
            print(noti)
            if noti == 'Login successfully':
                while True:
                    msg = input('Message (q for quit): ')
                    if (msg == 'q'):
                        break
                    send(connection, msg)
                send(connection, DISCONNECT_MESSAGE)
                time.sleep(1)
                print('Disconnect')
                return


start()
