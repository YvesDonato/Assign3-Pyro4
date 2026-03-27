import os
import socket


SOCKET_SERVER_HOST = os.getenv("SOCKET_SERVER_HOST", "socket-server")
SOCKET_SERVER_PORT = int(os.getenv("SOCKET_SERVER_PORT", "9999"))


def main():
    request = input("Enter operation (e.g., add 5 3): ").strip()
    if not request:
        print("No operation entered.")
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((SOCKET_SERVER_HOST, SOCKET_SERVER_PORT))
            client.sendall(request.encode("ascii"))
            response = client.recv(4096)
    except OSError as exc:
        print(f"Client error: {exc}")
        return

    try:
        message = response.decode("ascii")
    except UnicodeDecodeError:
        print("Client error: received a non-text response from the server")
        return

    if message.startswith("error:"):
        print(f"Server response: {message}")
    else:
        print(f"Result: {message}")


if __name__ == "__main__":
    main()
