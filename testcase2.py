import re
import socket
import threading
import time
from collections import OrderedDict


class HTTPServer:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

        # Create server
        self.server = socket.socket()
        self.server_address = (self.ip_address, self.port)
        self.server.bind(self.server_address)

        self.start()
        self.cache = OrderedDict()

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

        if "https" in path:
            http_response = "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: 1024\nConnection: Closed\n\n"
            http_response += "<h1>You requested HTTPS </h1>"
            http_response += "<h1>Currently this request is not available </h1>"
            http_response = http_response.encode('utf-8')
        else:
            http_response = self.checkCache(path, http_request)

        connection.send(http_response)
        connection.close()
        pass

    def checkCache(self, path, http_request):
        if path not in self.cache:
            http_response = self.getWebsiteData(path, http_request)
            if len(http_response) < 10000:
                self.cache[path] = http_response
                self.cache.move_to_end(path)
                if len(self.cache) > int(5):
                    self.cache.popitem(last=False)
        else:
            http_response = self.cache[path]
            self.cache.move_to_end(path)

        return http_response

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

    def getWebsiteData(self, path, http_request):

        domain_name = path.replace("http://", "").split("/")[0]
        domain_port = 80
        domain_address = (domain_name, domain_port)

        domain = socket.socket()
        domain.connect(domain_address)
        print(f"Connected to {domain_name} through port {domain_port}")

        domain.send(http_request)
        print("Http request has been sent to the domain")

        http_response = domain.recv(10000000)
        response = http_response.decode()
        # get total responce size
        required_size = self.getSize(response)

        while True:
            if len(http_response) > required_size - 100:
                break
            else:
                http_response += domain.recv(10000000)
        print(f"received {len(http_response)} size of bytes")
        return http_response

    @staticmethod
    def getSize(response):
        lines = response.splitlines()
        response_length = 0
        for line in lines:
            if "Content-Length" in line:
                response_length = int(re.findall("[0-9]+", line)[0])
                break
        return response_length


def main():
    HTTPServer('127.0.0.1', 8888)


if __name__ == "__main__":
    main()
