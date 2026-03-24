import Pyro4
import socket

# server = Pyro4.Proxy("PYRONAME:server@127.0.0.1:9090")
#
# server.add(1, 2) # call fun from server

HOST = "127.0.0.1"
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    client.sendall(message.encode("ascii"))
    response = client.recv(4096)

print(response.decode("ascii"))
