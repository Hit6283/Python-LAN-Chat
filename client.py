import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

HOST = "127.0.0.1"
PORT = 55555

# Client setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# GUI setup
root = tk.Tk()
root.title("LAN Chat App")
root.geometry("400x500")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(root, width=50)
entry.pack(padx=10, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

mute = False

def write(msg):
    chat_area.config(state='normal')
    chat_area.insert(tk.END, msg + "\n")
    chat_area.yview(tk.END)
    chat_area.config(state='disabled')

def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "USERNAME":
                client.send(username.encode("utf-8"))
            else:
                if not mute:
                    write(message)
        except:
            write("Disconnected from server")
            client.close()
            break

def send():
    msg = entry.get()
    entry.delete(0, tk.END)

    if msg.startswith("/mute"):
        global mute
        mute = True
        write("🔇 You muted messages.")
        return
    elif msg.startswith("/unmute"):
        mute = False
        write("🔊 You unmuted messages.")
        return
    elif msg.startswith("/exit"):
        client.send(f"{username} left the chat. /exit".encode("utf-8"))
        root.destroy()
        client.close()
        return

    client.send(f"{username}: {msg}".encode("utf-8"))

send_button = tk.Button(root, text="Send", command=send)
send_button.pack(padx=5, pady=5, side=tk.RIGHT)

# Get username before starting
username = simpledialog.askstring("Username", "Enter your name:", parent=root)

# Start thread to receive messages
thread = threading.Thread(target=receive)
thread.daemon = True
thread.start()

root.mainloop()
