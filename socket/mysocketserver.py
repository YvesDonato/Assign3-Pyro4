import Pyro4
import socket

server = Pyro4.Proxy("PYRONAME:server")

server.add(1, 2) # call fun from server