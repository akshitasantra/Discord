import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []

class Client:
    def __init__(self, connection, name):
        self.connection = connection
        self.name = name

def broadcast(message):
    for client in clients:
        client.connection.send(message.encode('ascii'))

def send_user_list():
    user_list = ", ".join([c.name for c in clients])
    for client in clients:
        client.connection.send((f"USERS:, {user_list}").encode('ascii'))

def handle(client):
    while True:
        try:
            nickname = client.name
            message = client.connection.recv(1024).decode('ascii')
            if message == 'LIST':
                send_user_list(client)
            else:
                message = '{}: {}'.format(nickname, message)
                broadcast(message)
        except:
            nickname = client.name
            client.connection.close()
            clients.remove(client)
            broadcast('{} left!'.format(nickname))
            send_user_list()
            break


def receive():
    while True:
        connection, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Send 'OK' response to indicate readiness to receive the 'NICK' message
        connection.send('OK'.encode('ascii'))
        # Now receive the nickname
        nickname = connection.recv(1024).decode('ascii')
        client = Client(connection, nickname)
        clients.append(client)

        print("Nickname is {}".format(nickname))
        broadcast("{} joined!\n".format(nickname))

        thread = threading.Thread(target=handle, args=(client,))
        send_user_list()
        thread.start()


print("Server is running!")
receive()