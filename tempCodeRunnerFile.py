
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
                while True:
                    msg = receive(conn)
                    send(conn, msg)
