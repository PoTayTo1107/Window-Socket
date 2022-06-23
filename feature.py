


post = {
    "name": "Khoa"
}

def start():
    answer = input('Would you like to connect (yes/no)? ')
    if answer.lower() != 'yes':
        return
    
    connection = connect()
    while True:
        msg = input("Message (q for quit): ")
        
        if (msg == 'q'):
            break
        
        send(connection, msg)
        
    send(connection, DISCONNECT_MESSAGE)
    time.sleep(1)
    print('Disconnect')
    
start()

