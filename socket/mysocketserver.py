import Pyro4
import os
import socket
import threading
import time


PYRO_NS_HOST = os.getenv("PYRO_NS_HOST", "127.0.0.1")
PYRO_NS_PORT = int(os.getenv("PYRO_NS_PORT", "9090"))
SOCKET_SERVER_BIND_HOST = os.getenv("SOCKET_SERVER_BIND_HOST", "0.0.0.0")
SOCKET_SERVER_PORT = int(os.getenv("SOCKET_SERVER_PORT", "9999"))


def create_pyro_proxy():
    last_error = None
    for _ in range(10):
        try:
            nameserver = Pyro4.locateNS(host=PYRO_NS_HOST, port=PYRO_NS_PORT)
            uri = nameserver.lookup("server")
            return Pyro4.Proxy(uri)
        except Exception as exc:
            last_error = exc
            time.sleep(1)

    raise RuntimeError(
        f"Unable to connect to Pyro nameserver at {PYRO_NS_HOST}:{PYRO_NS_PORT}"
    ) from last_error


def call_remote(method_name, *operands):
    with create_pyro_proxy() as pyro_server:
        return getattr(pyro_server, method_name)(*operands)


def add(op1, op2):
    return call_remote("add", op1, op2)


def sub(op1, op2):
    return call_remote("sub", op1, op2)


def mult(op1, op2):
    return call_remote("mult", op1, op2)


def div(op1, op2):
    return call_remote("div", op1, op2)


def mod(op1, op2):
    return call_remote("mod", op1, op2)


def sqrt(op1):
    return call_remote("sqrt", op1)


def usage_for(command, expected_count):
    if expected_count == 1:
        return f"incorrect syntax; use: {command} <number>"

    return f"incorrect syntax; use: {command} <number> <number>"


def parse_operands(parts, command, expected_count):
    if len(parts) != expected_count + 1:
        raise ValueError(usage_for(command, expected_count))

    try:
        return [float(value) for value in parts[1:]]
    except ValueError as exc:
        raise ValueError("operands must be numeric") from exc


def format_result(result):
    if isinstance(result, float) and result.is_integer():
        return str(int(result))

    return str(result)


def handle_request(message: str):
    parts = message.strip().split()
    if not parts:
        return "error: empty request"

    command = parts[0].lower()

    try:
        if command == "add":
            operands = parse_operands(parts, command, 2)
            result = add(*operands)
        elif command == "sub":
            operands = parse_operands(parts, command, 2)
            result = sub(*operands)
        elif command == "mult":
            operands = parse_operands(parts, command, 2)
            result = mult(*operands)
        elif command == "div":
            operands = parse_operands(parts, command, 2)
            if operands[1] == 0:
                return "error: division by zero"
            result = div(*operands)
        elif command == "mod":
            operands = parse_operands(parts, command, 2)
            if operands[1] == 0:
                return "error: modulo by zero"
            result = mod(*operands)
        elif command == "sqrt":
            operands = parse_operands(parts, command, 1)
            if operands[0] < 0:
                return "error: square root requires a non-negative number"
            result = sqrt(*operands)
        else:
            return "error: unknown command"
    except ValueError as exc:
        return f"error: {exc}"
    except Exception as exc:
        return f"error: {exc}"

    return format_result(result)


def send_response(conn, response):
    conn.sendall(response.encode("ascii"))


def handle_client(conn, addr):
    with conn:
        print(f"Connected by {addr} on thread {threading.current_thread().name}")

        try:
            data = conn.recv(4096)
            if not data:
                print(f"Client {addr} disconnected without sending data")
                return

            try:
                message = data.decode("ascii").strip()
            except UnicodeDecodeError:
                send_response(conn, "error: request must use ascii text")
                return

            print("Received:", message)
            response = handle_request(message)
            send_response(conn, response)
        except OSError as exc:
            print(f"Socket error while handling {addr}: {exc}")
        except Exception as exc:
            print(f"Unexpected error while handling {addr}: {exc}")
            try:
                send_response(conn, "error: internal server error")
            except OSError:
                pass


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_server:
        tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_server.bind((SOCKET_SERVER_BIND_HOST, SOCKET_SERVER_PORT))
        tcp_server.listen()

        print(f"Listening on {SOCKET_SERVER_BIND_HOST}:{SOCKET_SERVER_PORT}")

        while True:
            conn, addr = tcp_server.accept()
            client_thread = threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True,
            )
            client_thread.start()


if __name__ == "__main__":
    main()
