import socket
import time
import os
import threading
import tkinter
import tkinter.scrolledtext
import tkinter.messagebox
from tkinter import *
import PIL
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

        self.login_thread = threading.Thread(target=self.login_signup_picker)
        self.login_thread.start()

    def login_signup_picker(self):
        global tk
        tk = Tk()
        tk.iconbitmap('imgs/notes.ico')
        tk.title("E-note")
        tk.config(bg='#fff')

        self.img = ImageTk.PhotoImage(file="imgs/Notes.jpeg")
        self.label = Label(tk, image=self.img).place(x=10, y=5)

        self.login_button = Button(tk, text=' Log in ', command=lambda:
                                   (tk.destroy(),
                                    self.login_form()))
        self.login_button.place(x=135, y=25)

        self.signup_button = Button(tk, text='Sign up', command=lambda:
                                    (tk.destroy(),
                                     self.signup_form()))
        self.signup_button.place(x=135, y=65)

        tk.mainloop()

    def login_form(self):
        global tk
        tk = Tk()
        tk.title("Log In")

        Label(tk, text="Username: ").grid(column=0, row=0, sticky=W)
        Label(tk, text="Password: ").grid(column=0, row=1, sticky=W)

        self.username = Entry(tk)
        self.username.grid(column=1, row=0, pady=2)
        self.username.focus_set()

        self.password = Entry(tk, show='*')
        self.password.grid(column=1, row=1, pady=2)
        self.username.bind('<Return>', lambda x: self.password.focus_set())

        self.button = Button(tk, text=' Log in ', command=lambda:
                             (self.send(self.username.get()),
                              self.send(self.password.get()),
                              tk.destroy()))
        self.button.grid(column=0, row=2, columnspan=2, pady=5)
        self.password.bind('<Return>', lambda x: self.button.invoke())

        tk.mainloop()

        if self.creds:
            self.send(self.creds)

    def signup_form(self):
        global tk
        tk = Tk()
        tk.title("Sign Up")

        Label(tk, text="Username: ").grid(column=0, row=0, sticky=W)
        Label(tk, text="Password: ").grid(column=0, row=1, sticky=W)

        self.username = Entry(tk)
        self.username.grid(column=1, row=0, pady=2)
        self.username.focus_set()

        self.password = Entry(tk, show='*')
        self.password.grid(column=1, row=1, pady=2)
        self.username.bind('<Return>', lambda: self.password.focus_set())

        self.button = Button(tk, text='Sign up',
                             command=lambda: (self.signupExe()))
        self.button.grid(column=0, row=2, columnspan=2, pady=5)
        self.password.bind('<Return>', lambda: self.button.invoke())

        tk.mainloop()

    def gui_loop(self):
        self.win = Tk()
        self.win.configure(bg="lightgray")

        self.chat_label = Label(self.win, text='Chat: ', bg="lightgray")
        self.chat_label.config(state='disabled')
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.config(font=("Arial", 12))
        self.text_area.pack(padx=20, pady=5)

        self.msg_label = Label(self.win, text='Message: ', bg="lightgray")
        self.msg_label.config(state='disabled')
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = Button(self.win, text='Send', command=self.write)
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
        self.sock.send(msg.encode(FORMAT))

    def receive(self):
        return self.sock.recv(2048).decode(FORMAT)

    def signupExe(self):
        username = self.username.get()
        password = self.password.get()
        list = str(["Sign up", username, password])
        self.send(list)
        out = self.receive()
        print(out)
        if out == "0":
            tkinter.messagebox.showinfo(
                "Notification", "Sign up successfully")
        elif out == "1":
            tkinter.messagebox.showerror(
                "Notification", "Username is too short")
        elif out == "2":
            tkinter.messagebox.showerror(
                "Notification", "Password is too short")
        elif out == "3":
            tkinter.messagebox.showerror(
                "Notification", "Username contains invalid character(s)")
        elif out == "4":
            tkinter.messagebox.showerror(
                "Notification", "Username is already taken")
        else:
            tkinter.messagebox.showerror(
                "Notification", "ERROR!")

        tk.destroy()
        self.login_signup_picker()

    def sendNote(self):
        print(self.receive)
        self.send(input())
        print(self.receive)
        self.cont

    def recvNote(self):
        print(self.receive)
        self.cont


client = Client()
