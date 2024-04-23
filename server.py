# server.py
import socket
import subprocess

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "127.0.0.1"
port = 9990

server_socket.bind((host, port))

server_socket.listen(5)

print("Waiting for the client connection.......")

client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

message = "Welcome to the game! You are now connected."
client_socket.send(message.encode())

print("Running app.py...")
subprocess.run(["python", "app.py"])

client_socket.close()

server_socket.close()
