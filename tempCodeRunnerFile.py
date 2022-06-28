global tk
        tk = Tk()
        tk.iconbitmap('imgs/notes.ico')
        tk.title("E-note")
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
                             command=lambda: (self.signupExe()))
        self.addnote_btn.place(x=625, y=200)
        
        self.addimg_btn_img = ImageTk.PhotoImage(file="imgs/SignBtn.png")
        self.addimg_btn = Button(tk, image=self.addimg_btn_img,
                             borderwidth=0, highlightthickness=0,
                             command=lambda: (self.signupExe()))
        self.addimg_btn.place(x=625, y=260)
        
        self.addfile_btn_img = ImageTk.PhotoImage(file="imgs/SignBtn.png")
        self.addfile_btn = Button(tk, image=self.addfile_btn_img,
                             borderwidth=0, highlightthickness=0,
                             command=lambda: (self.signupExe()))
        self.addfile_btn.place(x=625, y=320)
        
        tk.protocol("WM_DELETE_WINDOW", self.stop)
        tk.mainloop()