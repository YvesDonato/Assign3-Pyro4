import Pyro4
import os
import time

class Server:
    # @Pyro4.expose, means that the preceding method will be remotely accessible.
    @Pyro4.expose
    def add(self, op1, op2):
        try:
            return op1 + op2
        except Exception as e:
            return e

    @Pyro4.expose
    def sub(self, op1, op2):
        try:
            return op1 - op2
        except Exception as e:
            return e

    @Pyro4.expose
    def mult(self, op1, op2):
        try:
            return op1 * op2
        except Exception as e:
            return e

    @Pyro4.expose
    def div(self, op1, op2):
        try:
            return op1 / op2
        except Exception as e:
            return e

    @Pyro4.expose
    def mod(self, op1, op2):
        try:
            return op1 % op2
        except Exception as e:
            return e

    @Pyro4.expose
    def sqrt(self, op1):
        try:
            return op1 ** 0.5
        except Exception as e:
            return e

def startServer():
    # Next, build the server instance of the Server class:
    server = Server()
    pyro_bind_host = os.getenv("PYRO_BIND_HOST", "0.0.0.0")
    pyro_public_host = os.getenv("PYRO_PUBLIC_HOST", "pyro-server")
    pyro_port = int(os.getenv("PYRO_SERVER_PORT", "9091"))
    ns_host = os.getenv("PYRO_NS_HOST", "127.0.0.1")
    ns_port = int(os.getenv("PYRO_NS_PORT", "9090"))

    # Then, define the Pyro4 daemon:
    daemon = Pyro4.Daemon(
        host=pyro_bind_host,
        port=pyro_port,
        nathost=pyro_public_host,
        natport=pyro_port,
    )

    # Retry nameserver discovery because depends_on does not guarantee readiness.
    last_error = None
    for _ in range(10):
        try:
            ns = Pyro4.locateNS(host=ns_host, port=ns_port)
            break
        except Exception as exc:
            last_error = exc
            time.sleep(1)
    else:
        raise RuntimeError(
            f"Unable to connect to Pyro nameserver at {ns_host}:{ns_port}"
        ) from last_error

    # Register the object server as Pyro object; it will only be known inside the Pyro daemon:
    uri = daemon.register(server)
    # Now, we can register the object server with a name in the nameserver:
    ns.register("server", uri)

    # The function ends with a call to the daemon's request Loop method. This starts the event loop of the server and
    # waits for calls:
    print("Ready. Object uri =", uri)
    daemon.requestLoop()

if __name__ == "__main__":
    startServer()
