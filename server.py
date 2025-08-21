import socket
import threading
import datetime

# Server config
HOST = "127.0.0.1"   # Localhost for LAN; replace with your IP for LAN test
PORT = 55555

# Store clients
clients = []
usernames = []

# Log file
LOG_FILE = "chat_logs.txt"

def log_message(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def broadcast(message, client=None):
    for c in clients:
        if c != client:  # Don’t send to sender
            c.send(message)

def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                break

            decoded_msg = msg.decode("utf-8")
            log_message(decoded_msg)

            if decoded_msg.endswith("/exit"):
                index = clients.index(client)
                username = usernames[index]
                broadcast(f"{username} left the chat.".encode("utf-8"), client)
                log_message(f"{username} left the chat.")
                clients.remove(client)
                usernames.remove(username)
                client.close()
                break

            broadcast(msg, client)
        except:
            # On error, remove client
            if client in clients:
                index = clients.index(client)
                username = usernames[index]
                broadcast(f"{username} disconnected.".encode("utf-8"), client)
                log_message(f"{username} disconnected.")
                clients.remove(client)
                usernames.remove(username)
            client.close()
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("USERNAME".encode("utf-8"))
        username = client.recv(1024).decode("utf-8")

        usernames.append(username)
        clients.append(client)

        print(f"Username: {username}")
        log_message(f"{username} joined the chat.")

        broadcast(f"{username} joined the chat.".encode("utf-8"))
        client.send("Connected to server.".encode("utf-8"))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server running...")
receive()
