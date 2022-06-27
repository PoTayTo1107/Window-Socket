import socket
import gc
import time
import os
import threading
import tkinter as tk
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


class Client:

    def __init__(self):
        os.system('cls')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(ADDR)

        self.gui_done = False

        self.login_thread = threading.Thread(target=self.login_signup_picker)
        self.login_thread.start()

    def login_signup_picker(self):
        global tk
        tk = Tk()
        tk.iconbitmap('imgs/notes.ico')
        tk.title("E-note")
        tk.config(bg='white')
        tk.resizable(False, False)

        window_height = 500
        window_width = 900
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        tk.geometry("{}x{}+{}+{}".format(window_width,
                    window_height, x_cordinate, y_cordinate))

        self.img = ImageTk.PhotoImage(file="imgs/Home.jpg")
        self.label = Label(tk, image=self.img).place(x=0, y=0)

        Label(tk, text="E-Note", bg="white",
              font=("Times New Roman", 60, "bold")).place(x=590, y=120)

        self.login_btn = ImageTk.PhotoImage(file="imgs/LogBtn.png")
        self.login_button = Button(tk, image=self.login_btn, borderwidth=0,
                                   command=lambda: (tk.destroy(),
                                                    self.login_form()))
        self.login_button.place(x=530, y=270)

        self.signup_btn = ImageTk.PhotoImage(file="imgs/SignBtn.png")
        self.signup_button = Button(tk, image=self.signup_btn, borderwidth=0,
                                    command=lambda: (tk.destroy(),
                                                     self.signup_form()))
        self.signup_button.place(x=730, y=270)

        tk.mainloop()

    def loginExe(self):
        username = self.username.get()
        password = self.password.get()
        list = str(["Log in", username, password])
        self.send(list)
        out = self.receive()
        if out == "0":
            tkinter.messagebox.showinfo(
                "Notification", "Log in successfully")
            tk.destroy()
            self.nickname = username
            self.gui_loop(),
        else:
            tkinter.messagebox.showerror(
                "Notification", "Invalid username or password")

    def login_form(self):
        global tk
        tk = Tk()
        tk.title("Log In")
        tk.resizable(False, False)

        window_height = 500
        window_width = 900
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        tk.geometry("{}x{}+{}+{}".format(window_width,
                    window_height, x_cordinate, y_cordinate))

        Label(tk, text="Username: ").grid(column=0, row=0)
        Label(tk, text="Password: ").grid(column=0, row=1)

        self.username = Entry(tk)
        self.username.grid(column=1, row=0, pady=2)
        self.username.focus_set()

        self.password = Entry(tk, show='*')
        self.password.grid(column=1, row=1, pady=2)
        self.username.bind('<Return>', lambda: self.password.focus_set())

        self.button = Button(tk, text=' Log in ',
                             command=lambda: (self.loginExe()))
        self.button.grid(column=0, row=2, columnspan=2, pady=5)
        self.password.bind('<Return>', lambda: self.button.invoke())

        tk.mainloop()

    def signupExe(self):
        username = self.username.get()
        password = self.password.get()
        list = str(["Sign up", username, password])
        self.send(list)
        out = self.receive()
        if out == "0":
            tkinter.messagebox.showinfo(
                "Notification", "Sign up successfully")
            tk.destroy()
            self.login_signup_picker()
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

    def signup_form(self):
        global tk
        tk = Tk()
        tk.title("Sign Up")
        tk.resizable(False, False)

        window_height = 500
        window_width = 900
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        tk.geometry("{}x{}+{}+{}".format(window_width,
                    window_height, x_cordinate, y_cordinate))

        Label(tk, text="Username: ").grid(column=0, row=0)
        Label(tk, text="Password: ").grid(column=0, row=1)

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
        global tk
        tk = Tk()
        tk.iconbitmap('imgs/notes.ico')
        tk.title("E-note")
        tk.config(bg='lightgray')
        tk.resizable(False, False)

        window_height = 620
        window_width = 800
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        tk.geometry("{}x{}+{}+{}".format(window_width,
                    window_height, x_cordinate, y_cordinate))

        self.chat_label = Label(tk, text='Chat: ', bg="lightgray")
        self.chat_label.config(state='disabled')
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(tk)
        self.text_area.config(font=("Arial", 12))
        self.text_area.pack(padx=20, pady=5)

        self.msg_label = Label(tk, text='Message: ', bg="lightgray")
        self.msg_label.config(state='disabled')
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = Text(tk, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = Button(tk, text='Send', command=lambda:
                                  (self.send(f"{self.nickname}: {self.input_area.get('1.0','end')}"),
                                   self.input_area.delete('1.0', END),
                                   self.receiveGui()))
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        tk.protocol("WM_DELETE_WINDOW", self.stop)

        tk.mainloop()

    def stop(self):
        tk.destroy()
        self.sock.close()
        exit()

    def receiveGui(self):
        message = self.receive()
        if self.gui_done:
            self.text_area.config(state='normal')
            self.text_area.insert('end', message)
            self.text_area.yview('end')
            self.text_area.config(state='disabled')
        elif ConnectionAbortedError:
            return
        else:
            self.sock.close()
            return

    def send(self, msg):
        self.sock.send(msg.encode(FORMAT))

    def receive(self):
        return self.sock.recv(2048).decode(FORMAT)


client = Client()
