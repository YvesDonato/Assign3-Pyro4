import Pyro4
import socket

pyro_server = Pyro4.Proxy("PYRONAME:server@127.0.0.1:9090")


def add(op1, op2):
    return pyro_server.add(op1, op2)

def sub(op1, op2):
    return pyro_server.sub(op1, op2)

def mult(op1, op2):
    return pyro_server.mult(op1, op2)

def div(op1, op2):
    return pyro_server.div(op1, op2)

def mod(op1, op2):
    return pyro_server.mod(op1, op2)

def sqrt(op1):
    return pyro_server.sqrt(op1)


def handle_request(message: str):
    parts = message.strip().split()
    command = parts[0].lower()

    if command == "add":
        result = add(float(parts[1]), float(parts[2]))
    elif command == "sub":
        result = sub(float(parts[1]), float(parts[2]))
    elif command == "mult":
        result = mult(float(parts[1]), float(parts[2]))
    elif command == "div":
        result = div(float(parts[1]), float(parts[2]))
    elif command == "mod":
        result = mod(float(parts[1]), float(parts[2]))
    elif command == "sqrt":
        result = sqrt(float(parts[1]))
    else:
        result = "unknown command"

    return str(result)


HOST = "127.0.0.1"
PORT = 9092

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_server:
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server.bind((HOST, PORT))
    tcp_server.listen()

    print(f"Listening on {HOST}:{PORT}")

    while True:
        conn, addr = tcp_server.accept()
        with conn:
            print("Connected by", addr)

            data = conn.recv(4096)
            if not data:
                continue

            message = data.decode("ascii").strip()
            print("Received:", message)

            response = handle_request(message)
            conn.sendall(response.encode("ascii"))
