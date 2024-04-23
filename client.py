# client.py
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "127.0.0.1"

port = 9990


client_socket.connect((host, port))

print("Connected to server!")

data = client_socket.recv(1024).decode()

print(data)

client_socket.close()
