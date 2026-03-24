import Pyro4

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

    # Then, define the Pyro4 daemon:
    daemon = Pyro4.Daemon()

    # To execute this script, we must run a Pyro4 statement to locate a nameserver:
    ns = Pyro4.locateNS()

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