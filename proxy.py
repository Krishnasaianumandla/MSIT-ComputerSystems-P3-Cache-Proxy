import socket
import threading


class HTTPServer:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

        # Create server
        self.server = socket.socket()
        self.server_address = (self.ip_address, self.port)
        self.server.bind(self.server_address)

        self.start()

    pass

    def start(self):
        self.server.listen()
        while True:
            connection, client_address = self.server.accept()
            thread = threading.Thread(target=self.handleClient, args=(connection,))
            thread.start()
            thread.join()

        pass

    def handleClient(self, connection):
        # receive HTTP Request
        http_request = connection.recv(1024)
        http_request_decoded = http_request.decode('utf-8')
        request_method, path, version = self.getRequestLine(http_request_decoded)

        # find domain ip address
        ip_address = self.getDomainAddress(path)
        port = 80
        domain_address = (ip_address, port)
        domain = socket.socket()
        # self.server.connect(domain_address)
        domain.connect(domain_address)
        domain.send(http_request)

        http_response = None
        while True:
            data = domain.recv(1024)
            print("receiving data")
            if len(data) == 0:
                break
            http_response += data

        print("DONE!!! received data")

        connection.send(http_response)
        connection.close()
        pass

    @staticmethod
    def getRequestLine(http_request):
        # split lines into list
        lines = http_request.splitlines()

        # Extract request line details
        request_line = lines[0].split(" ")
        request_method = request_line[0]
        path = request_line[1]
        version = request_line[2]
        return request_method, path, version
        pass

    @staticmethod
    def getDomainAddress(path):
        path = path.replace("http://", "www.")
        domain_address = socket.gethostbyname(path)
        return domain_address


def main():
    HTTPServer('127.0.0.1', 8888)


if __name__ == "__main__":
    main()
