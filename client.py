import socket
import time
import tkinter
import tkinter.scrolledtext
import threading
from tkinter import simpledialog
from email import message
from http import client

PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "26.183.40.49"
ADDR = (SERVER, PORT)


# def gui_loop(conn):
#     conn.win = tkinter.tk()
#     conn.win.configure(bg="lightgray")

#     conn.chat_label = tkinter.Label(
#         conn.win, text='Chat: ', bg="lightgray")
#     conn.chat_label.config(state='disabled')
#     conn.chat_label.pack(padx=20, pady=5)

#     conn.text_area = tkinter.scrolledtext.ScrolledText(conn.win)
#     conn.text_area.config(font=("Arial", 12))
#     conn.text_area.pack(padx=20, pady=5)

#     conn.msg_label = tkinter.Label(
#         conn.win, text='Message: ', bg="lightgray")
#     conn.msg_label.config(state='disabled')
#     conn.msg_label.pack(padx=20, pady=5)

#     conn.input_area = tkinter.Text(conn.win, height=3)
#     conn.input_area.pack(padx=20, pady=5)

#     conn.send_button = tkinter.Button(
#         conn.win, text='Send', command=conn.write)
#     conn.send_button.config(font=("Arial", 12))
#     conn.send_button.pack(padx=20, pady=5)

#     conn.gui_done = True

#     conn.win.protocol("WM_DELETE_WINDOW", conn.stop)

#     conn.win.mainloop()


# def write(conn):
#     message = f"{conn.nickname}: {conn.input_area.get('1.0','end')}"
#     send(conn, message)
#     conn.input_area.delete()


# def stop(conn):
#     conn.running = False
#     conn.win.destroy()
#     conn.sock.close()
#     exit(0)


# def receiveGui(conn):
#     pass


# def gui(conn):
#     msg = tkinter.tk()
#     msg.withdraw()

#     conn.nickname = simpledialog.askstring(
#         "Nickname", "Please choose nickname", parent=msg)

#     conn.gui_done = False
#     conn.running = True

#     gui_thread = threading.Thread(target=conn.gui_loop)
#     receive_thread = threading.Thread(target=conn.receiveGui)


def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client


def send(conn, msg):
    conn.sendall(msg.encode(FORMAT))


def recvPrint(conn):
    print(conn.recv(2048).decode(FORMAT))


def form(conn):
    recvPrint(conn)
    recvPrint(conn)
    send(conn, input())
    recvPrint(conn)
    send(conn, input())


def sendNote(conn):
    recvPrint(conn)
    send(conn, input())
    recvPrint(conn)
    print('\n')


def recvNote(conn):
    recvPrint(conn)


def start():
    answer = input('Would you like to connect (yes/no)?\n')
    if answer.lower() != 'yes':
        return

    conn = connect()

    while True:
        recvPrint(conn)
        rec = input()
        send(conn, rec)

        if rec.lower() == 'signup':
            form(conn)
            recvPrint(conn)

        if rec.lower() == 'login':
            form(conn)
            noti = conn.recv(2048).decode(FORMAT)
            print(noti)
            if noti == 'Login successfully':
                recvPrint(conn)
                func = input()
                send(conn, func)
                if func == "1":
                    sendNote(conn)
                elif func == "2":
                    recvNote(conn)
                elif func == "3":
                    return


start()
