while True:
    #     send(conn, "Would you like signup or login (signup/login)?")
    #     ans = conn.recv(2048).decode(FORMAT)
    #     if ans.lower() == "signup":
    #         signUpForm(conn)
    #     elif ans.lower() == "login":
    #         login, username = loginForm(conn)
    #         if login == 1:
    #             send(conn, "Login successfully")
    #             print(f"[NEW CONNECTION] {username} connected.")
    #             print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    #             while True:
    #                 sendFuncList(conn)
    #                 func = conn.recv(2048).decode(FORMAT)
    #                 if func == "1":
    #                     addNote(conn, "notes", username)
    #                     time.sleep(1)
    #                 elif func == "2":
    #                     showNote(conn, username)
    #                     time.sleep(1)
    #                 else:
    #                     conn.close()
    #                     print(f"[DISCONNECTION] {username} disconnected.")
    #                     print(
    #                         f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
    #                     return
    #         else:
    #             send(conn, "Invalid username or password")