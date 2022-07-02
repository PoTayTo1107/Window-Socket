import io
import socket
import os
import threading
import base64
import tkinter as tk
import tkinter.scrolledtext
import tkinter.messagebox
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from turtle import width
from PIL import ImageTk, Image
from tkinter import ttk

PORT = 5050
SERVER = "26.183.40.49"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


class Client:

    def __init__(self):
        # Clear screen
        os.system('cls')

        # IPv4 & TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server
        self.sock.connect(ADDR)

        self.eye_show = True

        # Start thread
        self.login_thread = threading.Thread(target=self.signup_form)
        self.login_thread.start()

    # LOGIN SIGNUP
    def eyeExe(self):
        # Hide/Show password button
        if self.eye_show == True:
            self.eye_show = False
            self.password.config(show="", font=("helvetica", 13))
        else:
            self.eye_show = True
            self.password.config(show="•", font=("helvetica", 16))

    def loginExe(self):
        # Get text from entry boxes
        username = self.username.get()
        password = self.password.get()

        # Send user's options & data to server
        list = str(["Log in", username, password])
        self.send(list)

        # Receive server's checking validation
        out = self.receive()
        if out == "0":
            tkinter.messagebox.showinfo(
                "Notification", "Log in successfully")
            tk.destroy()
            self.nickname = username

            # Receive data from server to show on next window
            self.notes = self.receive()
            self.notes = eval(self.notes)
            self.mainGui()
        else:
            tkinter.messagebox.showerror(
                "Error", "Invalid username or password")

    def login_form(self):
        # Create window
        global tk
        tk = Tk()
        tk.iconbitmap('imgs/notes.ico')
        tk.title("LOGIN")
        tk.config(bg='white')
        tk.resizable(False, False)
        tk.after(1, lambda: tk.focus_force())

        # Set up window size & center window
        window_height = 500
        window_width = 900
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        tk.geometry("{}x{}+{}+{}".format(window_width,
                    window_height, x_cordinate, y_cordinate))

        # Show background images
        self.img = ImageTk.PhotoImage(file="imgs/Home.jpg")
        Label(tk, image=self.img, borderwidth=0,
              highlightthickness=0).place(x=0, y=0)
        self.avatar = ImageTk.PhotoImage(file="imgs/avatar.png")
        Label(tk, image=self.avatar, borderwidth=0,
              highlightthickness=0).place(x=625, y=50)

        # Add labels
        Label(tk, text="LOG IN", bg="white", fg="#39c3e2",
              font=("helvetica", 20, "bold")).place(x=645, y=200)
        Label(tk, text="USERNAME: ", bg="white", fg="#39c3e2",
              font=("helvetica", 13, "bold")).place(x=530, y=250)
        Label(tk, text="PASSWORD: ", bg="white", fg="#39c3e2",
              font=("helvetica", 13, "bold")).place(x=530, y=290)

        # Add entry boxes
        self.username = Entry(tk, highlightthickness=0, relief=FLAT,
                              fg="#202124", font=("helvetica", 13))
        self.username.place(x=640, y=250)
        self.password = Entry(tk, show='•', highlightthickness=0,
                              relief=FLAT, fg="#202124", font=("helvetica", 16))
        self.password.place(x=640, y=290)

        # Add 2 lines below entry boxes for decoration
        username_line = Canvas(tk, width=190, height=1.0,
                               bg="#313131", highlightthickness=0)
        username_line.place(x=640, y=275)
        password_line = Canvas(tk, width=190, height=1.0,
                               bg="#313131", highlightthickness=0)
        password_line.place(x=640, y=315)

        # Show/Hide password button
        eye = ImageTk.PhotoImage(file="imgs/eyeshow.png")
        self.eye_button = Button(tk, image=eye, borderwidth=0,
                                 highlightthickness=0)
        self.eye_button.place(x=830, y=290)
        self.eye_button.bind('<ButtonPress>', lambda event: self.eyeExe())

        # Log in button
        login_btn = ImageTk.PhotoImage(file="imgs/LogBtn.png")
        button = Button(tk, image=login_btn,
                        borderwidth=0, highlightthickness=0,
                        command=lambda: (self.loginExe()))
        button.place(x=625, y=345)

        # Log in to Sign up button
        sign_button = Button(tk, text='Want to join us? Sign up now', font=("helvetica", 11),
                             borderwidth=0, highlightthickness=0, bg="#fff",
                             command=lambda: (tk.destroy(), self.signup_form()))
        sign_button.place(x=603, y=400)
        sign_button_line = Canvas(tk, width=188, height=1.1,
                                  bg="#313131", highlightthickness=0)
        sign_button_line.place(x=608, y=420)

        # Exit
        tk.protocol("WM_DELETE_WINDOW", self.stop)
        tk.mainloop()

    def signupExe(self):
        # Get text from entry boxes
        username = self.username.get()
        password = self.password.get()

        # Send user's options & data to server
        list = str(["Sign up", username, password])
        self.send(list)

        # Receive server's checking validation
        out = self.receive()
        if out == "0":
            tkinter.messagebox.showinfo(
                "Notification", "Sign up successfully")
            tk.destroy()
            self.login_form()
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
        # Create window
        global tk
        tk = Tk()
        tk.iconbitmap('imgs/notes.ico')
        tk.title("SIGN UP")
        tk.config(bg='white')
        tk.resizable(False, False)
        tk.after(1, lambda: tk.focus_force())

        # Set up window size & center window
        window_height = 500
        window_width = 900
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        tk.geometry("{}x{}+{}+{}".format(window_width,
                    window_height, x_cordinate, y_cordinate))

        # Show background images
        img = ImageTk.PhotoImage(file="imgs/Home.jpg")
        Label(tk, image=img, borderwidth=0,
              highlightthickness=0).place(x=0, y=0)

        avatar = ImageTk.PhotoImage(file="imgs/avatar.png")
        Label(tk, image=avatar, borderwidth=0,
              highlightthickness=0).place(x=625, y=50)

        # Add labels
        Label(tk, text="SIGN UP", bg="white", fg="#39c3e2",
              font=("helvetica", 20, "bold")).place(x=635, y=200)
        Label(tk, text="USERNAME: ", bg="white", fg="#39c3e2",
              font=("helvetica", 13, "bold")).place(x=530, y=250)
        Label(tk, text="PASSWORD: ", bg="white", fg="#39c3e2",
              font=("helvetica", 13, "bold")).place(x=530, y=290)

        # Add entry boxes
        self.username = Entry(tk, highlightthickness=0, relief=FLAT,
                              fg="#202124", font=("helvetica", 13))
        self.username.place(x=640, y=250)
        self.password = Entry(tk, highlightthickness=0, relief=FLAT,
                              fg="#202124", font=("helvetica", 13))
        self.password.place(x=640, y=290)

        # Add 2 lines below entry boxes for decoration
        username_line = Canvas(tk, width=190, height=1.0,
                               bg="#313131", highlightthickness=0)
        username_line.place(x=640, y=275)
        password_line = Canvas(tk, width=190, height=1.0,
                               bg="#313131", highlightthickness=0)
        password_line.place(x=640, y=315)

        # Sign up button
        self.login_btn = ImageTk.PhotoImage(file="imgs/SignBtn.png")
        self.button = Button(tk, image=self.login_btn,
                             borderwidth=0, highlightthickness=0,
                             command=lambda: (self.signupExe()))
        self.button.place(x=625, y=345)

        # Sign up to Log in button
        log_button = Button(tk, text='Already have an account?', font=("helvetica", 11),
                            borderwidth=0, highlightthickness=0, bg="#fff",
                            command=lambda: (tk.destroy(), self.login_form()))
        log_button.place(x=615, y=400)
        log_button_line = Canvas(
            tk, width=167, height=1.1, bg="#313131", highlightthickness=0)
        log_button_line.place(x=619, y=420)

        # Exit
        tk.protocol("WM_DELETE_WINDOW", self.stop)
        tk.mainloop()

    # ADD
    def addNoteExe(self):
        # Get data from user entry boxes
        title = self.input_title.get('1.0', 'end')
        message = self.input_area.get('1.0', 'end')

        # Send data to user and return to main GUI
        if title != "\n" and message != "\n":
            tk.destroy()  # Exit add GUI
            title = title[:-1]
            message = message[:-1]
            # Send data to server
            self.send(str(["Add", "Txt", title, message]))
            tkinter.messagebox.showinfo(
                "Notification", "Add text successfully")
            self.notes = self.receive()  # Receive updated data from server to show at mainGUI
            self.notes = eval(self.notes)
            self.mainGui()  # Return to main GUI
        else:
            tkinter.messagebox.showerror(
                "ERROR", "Cannot leave title or message empty!")

    def addNoteGuiExe(self):
        tk.destroy()
        self.mainGui()

    def addNoteGui(self):
        # Create window
        global tk
        tk = Tk()
        tk.iconbitmap('imgs/notes.ico')
        tk.title("ADD NOTE")
        tk.config(bg='#c5ebec')
        tk.resizable(False, False)
        tk.after(1, lambda: tk.focus_force())

        # Set up window size & center window
        window_height = 400
        window_width = 500
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2)) - 20
        tk.geometry("{}x{}+{}+{}".format(window_width,
                    window_height, x_cordinate, y_cordinate))

        # Add labels
        Label(tk, text="TITLE:", bg="#c5ebec", fg="#39c3e2",
              font=("helvetica", 13, "bold")).place(x=16, y=10)
        Label(tk, text="CONTENT:", bg="#c5ebec", fg="#39c3e2",
              font=("helvetica", 13, "bold")).place(x=16, y=65)

        # Entry boxes for adding note
        self.input_title = Text(tk, height=1, width=50, bg="#fff",
                                font=("Times New Roman", 13))
        self.input_title.place(x=20, y=35)
        self.input_area = Text(tk, height=13, width=50, bg="#fff",
                               font=("Times New Roman", 13))
        self.input_area.place(x=20, y=90)

        # Add note button
        send_note_button = Button(tk, text='Add',
                                  command=lambda: self.addNoteExe())
        send_note_button.config(font=("Helvetica", 13))
        send_note_button.place(x=430, y=355)

        # Exit
        tk.protocol("WM_DELETE_WINDOW", self.addNoteGuiExe)
        tk.mainloop()

    def addImgExe(self):
        # Get image directory from user
        img_path = askopenfilename(title='Select Image',
                                   filetypes=[("image", ".jpeg"),
                                              ("image", ".png"),
                                              ("image", ".jpg")])
        try:
            img = open(img_path, 'rb')  # Open image for reading later
            while img_path.find('/') > 0:
                # Get image name from img_path
                img_path = img_path[img_path.find('/')+1:]
            # Send user's option to server
            self.send(str(["Add", "Image", img_path]))
            img_data = img.read()  # Read and send image to server
            self.sock.send(img_data)
            img.close()
            tkinter.messagebox.showinfo(
                "Notification", "Add image successfully")
            tk.destroy()  # Exit AddGui and return to mainGui
            self.notes = self.receive()  # Receive updated data from server to show at mainGUI
            self.notes = eval(self.notes)
            self.mainGui()  # Return to mainGUI
        except:
            tkinter.messagebox.showerror(
                "ERROR", "Error while adding image")

    def addFileExe(self):
        # Get file directory from user
        file_path = askopenfilename(title='Select File')
        try:
            file = open(f'{file_path}', 'rb')  # Open file for reading later
            while file_path.find('/') > 0:
                # Get file name from file_path
                file_path = file_path[file_path.find('/')+1:]
            # Send user's option to server
            self.send(str(["Add", "File", file_path]))
            file_data = file.read()  # Read and send file to server
            self.sock.send(file_data)
            file.close()
            tkinter.messagebox.showinfo(
                "Notification", "Add file successfully")
            tk.destroy()  # Exit AddGui and return to mainGui
            self.notes = self.receive()  # Receive updated data from server to show at mainGUI
            self.notes = eval(self.notes)
            self.mainGui()  # Return to mainGUI
        except:
            tkinter.messagebox.showerror(
                "ERROR", "Error while adding file")

    def addExe(self):
        tk.destroy()
        self.mainGui()

    def addGui(self):
        # Create window
        global tk
        tk = Tk()
        tk.iconbitmap('imgs/notes.ico')
        tk.title("ADD")
        tk.config(bg='white')
        tk.resizable(False, False)
        tk.after(1, lambda: tk.focus_force())

        # Set up window size & center window
        window_height = 400
        window_width = 700
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        tk.geometry("{}x{}+{}+{}".format(window_width,
                    window_height, x_cordinate, y_cordinate))

        # Background image
        img = ImageTk.PhotoImage(file="imgs/Addhome.jpg")
        Label(tk, image=img, borderwidth=0,
              highlightthickness=0).place(x=0, y=0)

        # Label
        Label(tk, text="NOTE TYPES", bg="white", fg="#39c3e2",
              font=("helvetica", 25, "bold")).place(x=450, y=90)

        # Note types button
        add_note_btn_img = ImageTk.PhotoImage(file="imgs/Addnote.png")
        add_note_btn = Button(tk, image=add_note_btn_img,
                              borderwidth=0, highlightthickness=0,
                              command=lambda: (tk.destroy(), self.addNoteGui()))
        add_note_btn.place(x=480, y=160)

        add_img_btn_img = ImageTk.PhotoImage(file="imgs/Addimg.png")
        add_img_btn = Button(tk, image=add_img_btn_img,
                             borderwidth=0, highlightthickness=0,
                             command=lambda: (self.addImgExe()))
        add_img_btn.place(x=480, y=210)

        add_file_btn_img = ImageTk.PhotoImage(file="imgs/Addfile.png")
        add_file_btn = Button(tk, image=add_file_btn_img,
                              borderwidth=0, highlightthickness=0,
                              command=lambda: (self.addFileExe()))
        add_file_btn.place(x=480, y=260)

        # Exit
        tk.protocol("WM_DELETE_WINDOW", self.addExe)
        tk.mainloop()

    # SHOW
    def showNoteExe(self):
        tk.destroy()
        self.mainGui()

    def showNoteGui(self, title, msg):
        # Create window
        global tk
        tk = Tk()
        tk.iconbitmap('imgs/notes.ico')
        tk.title("SHOW NOTE")
        tk.config(bg='#c5ebec')
        tk.resizable(False, False)
        tk.after(1, lambda: tk.focus_force())

        # Set up window size & center window
        window_height = 400
        window_width = 500
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        tk.geometry("{}x{}+{}+{}".format(window_width,
                    window_height, x_cordinate, y_cordinate))

        # Add labels
        Label(tk, text="TITLE:", bg="#c5ebec", fg="#39c3e2",
              font=("helvetica", 13, "bold")).place(x=16, y=10)
        Label(tk, text="CONTENT:", bg="#c5ebec", fg="#39c3e2",
              font=("helvetica", 13, "bold")).place(x=16, y=65)

        # Create 2 text boxes for showing note content
        title_box = Text(tk, height=1, width=50, bg="#fff",
                         font=("Times New Roman", 13))
        title_box.place(x=20, y=35)
        title_box.insert('end', title)
        title_box.config(state='disabled')

        text_box = Text(tk, height=15, width=50, bg="#fff",
                        font=("Times New Roman", 13))
        text_box.place(x=20, y=90)
        text_box.insert('end', msg)
        text_box.config(state='disabled')

        # Exit
        tk.protocol("WM_DELETE_WINDOW", self.showNoteExe)
        tk.mainloop()

    def showImgExe(self):
        tk.destroy()
        self.mainGui()

    def showImgGui(self, width, height):
        # Create window
        global tk
        tk = Tk()
        tk.iconbitmap('imgs/notes.ico')
        tk.title("ADD NOTE")
        tk.config(bg='black')
        tk.resizable(False, False)
        tk.after(1, lambda: tk.focus_force())

        # Set up window size & center window
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        new_width = int(width * (screen_height/height))
        new_height = screen_height

        # Resize image to fit screen
        if height > screen_height:
            newsize = (new_width, new_height)
            self.buffer_image = self.buffer_image.resize(newsize)

        # Configure window size
        tk.geometry("{}x{}+{}+{}".format(screen_width,
                    screen_height, 0, 0))

        # Show image
        img = ImageTk.PhotoImage(self.buffer_image)
        Label(tk, image=img, borderwidth=0,
              highlightthickness=0).place(x=(screen_width-new_width)/2, y=(screen_height-new_height)/2)

        # Exit
        tk.protocol("WM_DELETE_WINDOW", self.showImgExe)
        tk.mainloop()

    def showExe(self):
        # Get current focused item
        selected_item = self.listNotes.focus()
        path = self.listNotes.item(selected_item, "values")
        if path[1] == "Txt":
            tk.destroy()
            self.showNoteGui(path[2], path[3])  # Show note
        elif path[1] == "Image":
            tk.destroy()
            self.send(str(["Show", path[3]]))  # Send user's option to server
            file = self.sock.recv(4096000)  # Receive & decode data
            buffer = io.BytesIO(base64.b64decode(file))
            self.buffer_image = Image.open(buffer)
            width, height = self.buffer_image.size  # Get image size
            self.showImgGui(width, height)  # Show image
        else:
            tkinter.messagebox.showerror(
                "ERROR", "Cannot show this type of note")  # Case item's type is file

    # DOWNLOAD
    def downloadExe(self):
        # Get current focused item
        selected_item = self.listNotes.focus()
        path = self.listNotes.item(selected_item, "values")
        if path[1] == "Txt":
            # Choose directory to save file
            dir = askdirectory(title='Select Folder')
            try:
                with open(f'{dir}/{path[2]}.txt', 'w') as file:
                    # Create new file & Write
                    file.write(path[3])
                file.close()
                tkinter.messagebox.showinfo(
                    "Notification", "Download note successfully")
            except:
                tkinter.messagebox.showerror(
                    "ERROR", "Error while downloading note")

        else:
            # Send user's option to server
            self.send(str(["Download", path[3]]))
            # Choose directory to save file
            dir = askdirectory(title='Select Folder')
            try:
                # Create new file & Write
                file = open(f"{dir}/{path[2]}", "wb")
                file_chunk = self.sock.recv(4096000)
                file.write(file_chunk)
                file.close()
                if path[1] == "Image":
                    tkinter.messagebox.showinfo(
                        "Notification", "Download image successfully")
                else:
                    tkinter.messagebox.showinfo(
                        "Notification", "Download file successfully")
            except:
                if path[1] == "Image":
                    tkinter.messagebox.showerror(
                        "ERROR", "Error while downloading image")
                else:
                    tkinter.messagebox.showerror(
                        "ERROR", "Error while downloading file")

    # MAIN GUI
    def mainGui(self):
        # Create window
        global tk
        tk = Tk()
        tk.iconbitmap('imgs/notes.ico')
        tk.title("E-note")
        tk.config(bg='white')
        tk.after(1, lambda: tk.focus_force())
        tk.resizable(False, False)

        # Set up window size & center window
        window_height = 500
        window_width = 600
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        tk.geometry("{}x{}+{}+{}".format(window_width,
                    window_height, x_cordinate, y_cordinate))

        # Create frame
        self.noteContainer = Frame(bg='#f2f2f2')
        self.noteContainer.place(x=40, y=30)

        # Treeview Scrollbar
        scrollBar = Scrollbar(self.noteContainer)
        scrollBar.pack(side=RIGHT, fill=Y)

        # Create Treeview
        self.listNotes = ttk.Treeview(
            self.noteContainer, height=20, yscrollcommand=scrollBar.set)
        self.listNotes.pack()

        # Treeview Style config
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("helvetica", 13, "bold"))
        style.configure("Treeview", font=(
            "helvetica", 13), foreground='#202124')

        # Scrollbar config
        scrollBar.config(command=self.listNotes.yview)

        # Tree view columns
        self.listNotes['columns'] = ("ID", "Type", "Title")
        self.listNotes.column("#0", width=0, stretch="NO")
        self.listNotes.column("ID", anchor="center", width=50)
        self.listNotes.column("Type", anchor="center", width=80)
        self.listNotes.column("Title", anchor="center", width=200)

        # Treeview headings
        self.listNotes.heading("#0", text="", anchor="center")
        self.listNotes.heading("ID", text="ID", anchor="center")
        self.listNotes.heading("Type", text="Type", anchor="center")
        self.listNotes.heading("Title", text="Title", anchor="center")

        # Add button
        add = ImageTk.PhotoImage(file="imgs/Add.png")
        add_btn = Button(tk, image=add,
                         borderwidth=0, highlightthickness=0,
                         command=lambda: (tk.destroy(), self.addGui()))
        add_btn.place(x=420, y=200)

        # Show button
        show = ImageTk.PhotoImage(file="imgs/Show.png")
        show_btn = Button(tk, image=show,
                          borderwidth=0, highlightthickness=0,
                          command=lambda: (self.showExe()))
        show_btn.place(x=420, y=250)

        # Download button
        download = ImageTk.PhotoImage(file="imgs/Download.png")
        download_btn = Button(tk, image=download,
                              borderwidth=0, highlightthickness=0,
                              command=lambda: (self.downloadExe()))
        download_btn.place(x=420, y=300)

        # Insert data to treeview
        count = 0
        for note in self.notes[self.nickname]:
            self.listNotes.insert(parent='', index='end', iid=count, text="",
                                  values=(count+1, note["type"], note["title"], note["content"]))
            count += 1

        # Set treeview focus to first note
        self.listNotes.focus_set()
        children = self.listNotes.get_children()
        if children:
            self.listNotes.focus(children[0])
            self.listNotes.selection_set(children[0])

        # Exit
        tk.protocol("WM_DELETE_WINDOW", self.stop)
        tk.mainloop()

    # Stop & Disconnect
    def stop(self):
        self.send(str([DISCONNECT_MESSAGE]))
        self.sock.close()
        exit(0)

    # Send
    def send(self, msg):
        self.sock.send(msg.encode(FORMAT))

    # Receive
    def receive(self):
        return self.sock.recv(2048).decode(FORMAT)


client = Client()
