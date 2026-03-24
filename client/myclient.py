import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999

client.connect((host, port))
data = client.recv(1024)
print("Server Time:", data.decode('ascii'))

client.close()