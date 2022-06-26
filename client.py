import socket
import time
import os
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import *
import PIL
import numpy
from PIL import ImageTk, Image
from pathlib import Path

PORT = 5050
SERVER = "26.183.40.49"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
FOLDER_PATH = r'C:/Users/anhkh/OneDrive/Documents/GitHub/Window-Socket'


class Client:

    def __init__(self):
        os.system('cls')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(ADDR)

        self.gui_done = False
        self.running = True

        login_thread = threading.Thread(target=self.login_signup_picker)
        login_thread.start()

        # gui_thread = threading.Thread(target=self.gui_loop)
        # receive_thread = threading.Thread(target=self.receiveGui)

        # gui_thread.start()
        # receive_thread.start()

    def login_signup_picker(self):
        self.tk = Tk()
        self.tk.iconbitmap('imgs/notes.ico')
        self.tk.title("E-note")
        self.tk.config(bg='#fff')
        self.tk.geometry('210x115')

        self.img = ImageTk.PhotoImage(file="imgs/Notes.jpeg")
        self.label = Label(self.tk, image=self.img).place(x=10, y=5)

        self.login_button = Button(self.tk, text=' Log in ', command=lambda:
                                   (lambda x: self.tk.destroy())
                                   )
        self.login_button.place(x=135, y=25)

        self.signup_button = Button(self.tk, text='Sign up', command=lambda:
                                    (lambda x: self.tk.destroy())
                                    )
        self.signup_button.place(x=135, y=65)

        self.tk.mainloop()

    def login_form(self):
        creds = []
        tk = Tk()
        tk.geometry('220x80')
        tk.title("Log In")

        Label(tk, text="Username: ").grid(column=0, row=0, sticky=W)
        Label(tk, text="Password: ").grid(column=0, row=1, sticky=W)

        username = Entry(tk)
        username.grid(column=1, row=0, pady=2)
        username.focus_set()

        password = Entry(tk, show='*')
        password.grid(column=1, row=1, pady=2)
        username.bind('<Return>', lambda x: password.focus_set())

        button = Button(tk, text='Log in!', command=lambda:
                        (lambda x: tk.destroy())
                        (creds.extend([username.get(), password.get()]))
                        )
        button.grid(column=0, row=2, columnspan=2, pady=5)
        password.bind('<Return>', lambda x: button.invoke())

        tk.mainloop()

        return creds if creds else None

    def signup_form(self):
        creds = []
        tk = Tk()
        tk.geometry('240x80')
        tk.title("Sign Up")

        Label(tk, text="Username: ").grid(column=0, row=0, sticky=W)
        Label(tk, text="Password: ").grid(column=0, row=1, sticky=W)

        username = Entry(tk)
        username.grid(column=1, row=0, pady=2)
        username.focus_set()

        password = Entry(tk, show='*')
        password.grid(column=1, row=1, pady=2)
        username.bind('<Return>', lambda x: password.focus_set())

        button = Button(tk, text='Log in!', command=lambda: (
            lambda x: tk.destroy())(creds.extend([username.get(), password.get()])))
        button.grid(column=0, row=2, columnspan=2, pady=5)
        password.bind('<Return>', lambda x: button.invoke())

        tk.mainloop()

        return creds if creds else None

    def gui_loop(self):
        self.win = Tk()
        self.win.configure(bg="lightgray")

        self.chat_label = Label(
            self.win, text='Chat: ', bg="lightgray")
        self.chat_label.config(state='disabled')
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.config(font=("Arial", 12))
        self.text_area.pack(padx=20, pady=5)

        self.msg_label = Label(
            self.win, text='Message: ', bg="lightgray")
        self.msg_label.config(state='disabled')
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = Button(
            self.win, text='Send', command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0','end')}"
        self.send(message)
        self.input_area.delete()

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receiveGui(self):
        while self.running:
            try:
                message = self.receive
                if message == 'NICK':
                    self.send(self.nickname)
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                self.sock.close()
                break

    def send(self, msg):
        self.sock.sendall(msg.encode(FORMAT))

    def receive(self):
        return self.sock.recv(2048).decode(FORMAT)

    def cont(self):
        input("Press Enter to Continue\n")

    def form(self):
        print(self.receive)
        self.send(input())
        print(self.receive)
        self.send(input())

    def sendNote(self):
        print(self.receive)
        self.send(input())
        print(self.receive)
        self.cont

    def recvNote(self):
        print(self.receive)
        self.cont

    def starting(self):
        while True:
            print(self.receive)
            rec = input()
            self.send(rec)

            if rec.lower() == "signup":
                self.form
                print(self.receive)

            if rec.lower() == "login":
                self.form
                noti = self.receive
                print(noti)
                self.cont
                if noti == "Login successfully":
                    while True:
                        print(self.receive)
                        func = input()
                        self.send(func)
                        if func == "1":
                            self.sendNote
                        elif func == "2":
                            self.recvNote
                        else:
                            input("DISCONNECTED!")
                            exit()


client = Client()
