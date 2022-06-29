import socket
import gc
import time
import os
import shutil
import threading
import tkinter as tk
import tkinter.scrolledtext
import tkinter.messagebox
from tkinter import *
from tkinter.filedialog import askopenfilename
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
        # path = askdirectory(title='Select Folder')
        self.login_thread = threading.Thread(target=self.login_signup_picker)
        self.login_thread.start()

    def login_signup_picker(self):
        global tk
        tk = Tk()
        tk.iconbitmap('imgs/notes.ico')
        tk.title("E-NOTE")
        tk.config(bg='white')
        tk.resizable(False, False)
        tk.after(1, lambda: tk.focus_force())

        window_height = 500
        window_width = 900
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        tk.geometry("{}x{}+{}+{}".format(window_width,
                    window_height, x_cordinate, y_cordinate))

        self.img = ImageTk.PhotoImage(file="imgs/Home.jpg")
        self.label = Label(tk, image=self.img, borderwidth=0,
                           highlightthickness=0).place(x=0, y=0)

        Label(tk, text="E-Note", bg="white", fg="#39c3e2",
              font=("Times New Roman", 60, "bold")).place(x=585, y=120)

        self.login_btn = ImageTk.PhotoImage(file="imgs/LogBtn.png")
        self.login_button = Button(tk, image=self.login_btn,
                                   borderwidth=0, highlightthickness=0,
                                   command=lambda: (tk.destroy(),
                                                    self.login_form()))
        self.login_button.place(x=530, y=270)

        self.signup_btn = ImageTk.PhotoImage(file="imgs/SignBtn.png")
        self.signup_button = Button(tk, image=self.signup_btn,
                                    borderwidth=0, highlightthickness=0,
                                    command=lambda: (tk.destroy(),
                                                     self.signup_form()))
        self.signup_button.place(x=720, y=270)

        tk.protocol("WM_DELETE_WINDOW", self.stop)
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
            self.functionGui(),
        else:
            tkinter.messagebox.showerror(
                "Error", "Invalid username or password")

    def login_form(self):
        global tk
        tk = Tk()
        tk.iconbitmap('imgs/notes.ico')
        tk.title("LOGIN")
        tk.config(bg='white')
        tk.resizable(False, False)
        tk.after(1, lambda: tk.focus_force())

        window_height = 500
        window_width = 900
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        tk.geometry("{}x{}+{}+{}".format(window_width,
                    window_height, x_cordinate, y_cordinate))

        self.img = ImageTk.PhotoImage(file="imgs/Home.jpg")
        Label(tk, image=self.img, borderwidth=0,
              highlightthickness=0).place(x=0, y=0)

        self.avatar = ImageTk.PhotoImage(file="imgs/avatar.png")
        Label(tk, image=self.avatar, borderwidth=0,
              highlightthickness=0).place(x=625, y=50)

        Label(tk, text="LOG IN", bg="white", fg="#39c3e2",
              font=("helvetica", 20, "bold")).place(x=645, y=200)

        Label(tk, text="USERNAME: ", bg="white", fg="#39c3e2",
              font=("helvetica", 13, "bold")).place(x=530, y=250)
        Label(tk, text="PASSWORD: ", bg="white", fg="#39c3e2",
              font=("helvetica", 13, "bold")).place(x=530, y=290)

        self.username = Entry(tk, highlightthickness=0, relief=FLAT,
                              fg="#202124", font=("helvetica", 13, "bold"))
        self.username.place(x=640, y=250)
        self.username_line = Canvas(
            tk, width=190, height=2.0, bg="#313131", highlightthickness=0)
        self.username_line.place(x=640, y=270)

        self.password = Entry(tk, show='*', highlightthickness=0,
                              relief=FLAT, fg="#202124", font=("helvetica", 13, "bold"))
        self.password.place(x=640, y=290)
        self.password_line = Canvas(
            tk, width=190, height=2.0, bg="#313131", highlightthickness=0)
        self.password_line.place(x=640, y=310)

        self.login_btn = ImageTk.PhotoImage(file="imgs/LogBtn.png")
        self.button = Button(tk, image=self.login_btn,
                             borderwidth=0, highlightthickness=0,
                             command=lambda: (self.loginExe()))
        self.button.place(x=625, y=345)

        tk.protocol("WM_DELETE_WINDOW", self.stop)
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
                "ERROR", "Username is too short")
        elif out == "2":
            tkinter.messagebox.showerror(
                "ERROR", "Password is too short")
        elif out == "3":
            tkinter.messagebox.showerror(
                "ERROR", "Username contains invalid character(s)")
        elif out == "4":
            tkinter.messagebox.showerror(
                "ERROR", "Username is already taken")
        else:
            tkinter.messagebox.showerror(
                "ERROR", "ERROR!")

    def signup_form(self):
        global tk
        tk = Tk()
        tk.iconbitmap('imgs/notes.ico')
        tk.title("SIGNUP")
        tk.config(bg='white')
        tk.resizable(False, False)
        tk.after(1, lambda: tk.focus_force())

        window_height = 500
        window_width = 900
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        tk.geometry("{}x{}+{}+{}".format(window_width,
                    window_height, x_cordinate, y_cordinate))

        self.img = ImageTk.PhotoImage(file="imgs/Home.jpg")
        Label(tk, image=self.img, borderwidth=0,
              highlightthickness=0).place(x=0, y=0)

        self.avatar = ImageTk.PhotoImage(file="imgs/avatar.png")
        Label(tk, image=self.avatar, borderwidth=0,
              highlightthickness=0).place(x=625, y=50)

        Label(tk, text="SIGN UP", bg="white", fg="#39c3e2",
              font=("helvetica", 20, "bold")).place(x=635, y=200)

        Label(tk, text="USERNAME: ", bg="white", fg="#39c3e2",
              font=("helvetica", 13, "bold")).place(x=530, y=250)
        Label(tk, text="PASSWORD: ", bg="white", fg="#39c3e2",
              font=("helvetica", 13, "bold")).place(x=530, y=290)

        self.username = Entry(tk, highlightthickness=0, relief=FLAT,
                              fg="#202124", font=("helvetica", 13, "bold"))
        self.username.place(x=640, y=250)
        self.username_line = Canvas(
            tk, width=190, height=2.0, bg="#313131", highlightthickness=0)
        self.username_line.place(x=640, y=270)

        self.password = Entry(tk, show='*', highlightthickness=0,
                              relief=FLAT, fg="#202124", font=("helvetica", 13, "bold"))
        self.password.place(x=640, y=290)
        self.password_line = Canvas(
            tk, width=190, height=2.0, bg="#313131", highlightthickness=0)
        self.password_line.place(x=640, y=310)

        self.login_btn = ImageTk.PhotoImage(file="imgs/SignBtn.png")
        self.button = Button(tk, image=self.login_btn,
                             borderwidth=0, highlightthickness=0,
                             command=lambda: (self.signupExe()))
        self.button.place(x=625, y=345)

        tk.protocol("WM_DELETE_WINDOW", self.stop)
        tk.mainloop()

    def functionGui(self):
        global tk
        tk = Tk()
        tk.iconbitmap('imgs/notes.ico')
        tk.title("FUNCTIONS")
        tk.config(bg='white')
        tk.resizable(False, False)
        tk.after(1, lambda: tk.focus_force())

        window_height = 500
        window_width = 900
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        tk.geometry("{}x{}+{}+{}".format(window_width,
                    window_height, x_cordinate, y_cordinate))

        self.img = ImageTk.PhotoImage(file="imgs/Home.jpg")
        Label(tk, image=self.img, borderwidth=0,
              highlightthickness=0).place(x=0, y=0)

        Label(tk, text="FUNCTIONS", bg="white", fg="#39c3e2",
              font=("helvetica", 40, "bold")).place(x=550, y=100)

        self.addnote_btn_img = ImageTk.PhotoImage(file="imgs/Addnote.png")
        self.addnote_btn = Button(tk, image=self.addnote_btn_img,
                                  borderwidth=0, highlightthickness=0,
                                  command=lambda: (tk.destroy(), self.addNoteGui()))
        self.addnote_btn.place(x=625, y=200)

        self.addimg_btn_img = ImageTk.PhotoImage(file="imgs/Addimg.png")
        self.addimg_btn = Button(tk, image=self.addimg_btn_img,
                                 borderwidth=0, highlightthickness=0,
                                 command=lambda: (self.addImgExe()))
        self.addimg_btn.place(x=625, y=260)

        self.addfile_btn_img = ImageTk.PhotoImage(file="imgs/Addfile.png")
        self.addfile_btn = Button(tk, image=self.addfile_btn_img,
                                  borderwidth=0, highlightthickness=0,
                                  command=lambda: (self.addFileExe()))
        self.addfile_btn.place(x=625, y=320)

        tk.protocol("WM_DELETE_WINDOW", self.disStop)
        tk.mainloop()

    def addNoteExe(self):
        title = self.input_title.get('1.0', 'end')
        message = self.input_area.get('1.0', 'end')
        if title != "\n" and message != "\n":
            self.input_title.delete('1.0', END)
            self.input_area.delete('1.0', END)
            tk.destroy()
            title = title[:-1]
            message = message[:-1]
            self.send(str(["note", title, message]))
            tkinter.messagebox.showinfo(
                "Notification", "Add text successfully")
            self.functionGui()
        else:
            tkinter.messagebox.showerror(
                "ERROR", "Cannot leave title or message empty!")

    def addNoteGui(self):
        global tk
        tk = Tk()
        tk.iconbitmap('imgs/notes.ico')
        tk.title("ADD NOTE")
        tk.config(bg='lightgray')
        tk.resizable(False, False)
        tk.after(1, lambda: tk.focus_force())

        window_height = 300
        window_width = 400
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2)) - 20
        tk.geometry("{}x{}+{}+{}".format(window_width,
                    window_height, x_cordinate, y_cordinate))

        self.input_title = Text(tk, height=1)
        self.input_title.pack(padx=20, pady=3)

        self.input_area = Text(tk, height=4)
        self.input_area.pack(padx=20, pady=5)

        self.send_note_button = Button(
            tk, text='Add', command=lambda: self.addNoteExe())
        self.send_note_button.config(font=("Arial", 12))
        self.send_note_button.pack(side=RIGHT, padx=20, pady=5)

        tk.protocol("WM_DELETE_WINDOW", self.disStop)

        tk.mainloop()

    def addImgExe(self):
        img_path = askopenfilename(title='Select Image',
                                   filetypes=[("image", ".jpeg"),
                                              ("image", ".png"),
                                              ("image", ".jpg")])
        try:
            shutil.copy(img_path, "userdata/imgs/")
            while img_path.find('/') > 0:
                img_path = img_path[img_path.find('/')+1:]
            self.send(str(["img", f"userdata/files/{img_path}"]))
            tkinter.messagebox.showinfo(
                "Notification", "Add image successfully")
        except:
            tkinter.messagebox.showerror(
                "ERROR", "Error while adding image")

    def addFileExe(self):
        file_path = askopenfilename(title='Select File')
        try:
            shutil.copy(file_path, "userdata/files/")
            while file_path.find('/') > 0:
                file_path = file_path[file_path.find('/')+1:]
            self.send(str(["file", f"userdata/files/{file_path}"]))
            tkinter.messagebox.showinfo(
                "Notification", "Add file successfully")
        except:
            tkinter.messagebox.showerror(
                "ERROR", "Error while adding file")

    # def showNoteExe(self):
    #     tk.destroy()
    #     self.text_area.config(state='normal')
    #    # self.text_area.insert('end', f"Title:\n{title}\nNote:\n{message}")
    #     self.text_area.yview('end')
    #     self.text_area.config(state='disabled')

    # def showNoteGui(self):
    #     global tk
    #     tk = Tk()
    #     tk.iconbitmap('imgs/notes.ico')
    #     tk.title("E-note")
    #     tk.config(bg='white')
    #     tk.resizable(False, False)
    #     tk.after(1, lambda: tk.focus_force())

    #     window_height = 700
    #     window_width = 800
    #     screen_width = tk.winfo_screenwidth()
    #     screen_height = tk.winfo_screenheight()
    #     x_cordinate = int((screen_width/2) - (window_width/2))
    #     y_cordinate = int((screen_height/2) - (window_height/2)) - 20
    #     tk.geometry("{}x{}+{}+{}".format(window_width,
    #                 window_height, x_cordinate, y_cordinate))

    #     self.chat_label = Label(tk, text='Chat: ', bg="lightgray")
    #     self.chat_label.config(state='disabled')
    #     self.chat_label.pack(padx=20, pady=5)

    #     self.text_area = Listbox(tk)
    #     self.text_area.config(font=("Arial", 12))
    #     self.text_area.pack(padx=20, pady=5)

    #     self.msg_label = Label(tk, text='Message: ', bg="lightgray")
    #     self.msg_label.config(state='disabled')
    #     self.msg_label.pack(padx=20, pady=5)

    #     self.send_img_button = Button(
    #         tk, text='Delete note', command=lambda: self.receiveNoteGui())
    #     self.send_img_button.config(font=("Arial", 12))
    #     self.send_img_button.pack(side=RIGHT, padx=20, pady=5)

    #     self.send_file_button = Button(
    #         tk, text='Show all notes', command=lambda: self.receiveNoteGui())
    #     self.send_file_button.config(font=("Arial", 12))
    #     self.send_file_button.pack(side=RIGHT, padx=20, pady=5)

    #     tk.protocol("WM_DELETE_WINDOW", self.disStop)

    #     tk.mainloop()

    def disStop(self):
        self.send(str([DISCONNECT_MESSAGE]))
        self.sock.close()
        exit(0)

    def stop(self):
        self.send(str([""]))
        self.sock.close()
        exit(0)

    def send(self, msg):
        self.sock.send(msg.encode(FORMAT))

    def receive(self):
        return self.sock.recv(2048).decode(FORMAT)

def sendFile_Client(client):
    try:
        file_path=input("File path: ")
        head_tail=os.path.split(file_path)
        file_name=head_tail[1]
        client.sendall(file_name.encode(FORMAT))
        file = open(file_path, 'rb')
        data = file.read(2048)
        while data:
            client.send(data)
            data = file.read(2048)
        file.close()
        print("Success")
    except:
        print("ERROR")
client = Client()
