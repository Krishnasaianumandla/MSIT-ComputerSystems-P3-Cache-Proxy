import re
import socket
import threading
from collections import OrderedDict


class HTTPServer:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

        # Create server
        self.server = socket.socket()
        self.server_address = (self.ip_address, self.port)
        self.server.bind(self.server_address)

        # create cache
        self.cache = OrderedDict()

        # Start server
        self.start()

    pass

    def start(self):
        self.server.listen()
        while True:
            # Accept clients
            connection, client_address = self.server.accept()
            thread = threading.Thread(target=self.handleClient, args=(connection,))
            thread.start()
            thread.join()

        pass

    def handleClient(self, connection):
        # receive client Request
        http_request = connection.recv(1024)
        http_request_decoded = http_request.decode('utf-8')

        # Extract Start line details
        request_method, path, version = self.getRequestLine(http_request_decoded)

        # check if client has requested https request
        if "https" in path:
            http_response = "HTTP/1.1 404 NOT FOUND\n\n"
            http_response = http_response.encode('utf-8')
        else:
            # check if path is in cache
            http_response = self.checkCache(path, http_request)

        # Send HTTP_Response and close the connection
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

    def checkCache(self, path, http_request):
        if path not in self.cache:
            # if path not in cache
            # create HTTP Response
            http_request = self.getHttpResponse(path, http_request)

            # check the size of the response. if less than 10000 bytes add to cache
            if len(http_request) < 10000:
                self.cache[path] = http_request
                self.cache.move_to_end(path)

                # check the size of cache. if the size exceeds then delete the less recently used
                if len(self.cache) > 5:
                    self.cache.popitem(last=False)

            return http_request

        else:
            # if path in cache get HTTP Response
            self.cache.move_to_end(path)
            return self.cache[path]

    def getHttpResponse(self, path, http_request):
        # get domain name with and without http://
        domain_name, neglect_text = self.getDomainAddress_path(path)
        domain_port = 80

        # connect to domain
        domain_address = (domain_name, domain_port)
        domain = socket.socket()
        domain.connect(domain_address)
        print(f"Connected to {domain_name} through port {domain_port}")

        # create HTTP_Request without domain name in the startline
        request_text = http_request.decode()
        request = request_text.replace(neglect_text, "")
        request_bytes = request.encode()

        # send the new HTTP_Request
        domain.send(request_bytes)
        print("Http request has been sent to the domain")

        # receive HTTP_Response form the domain
        http_response = domain.recv(10000000)
        response = http_response.decode()

        # extract get content-length from the response
        required_size = self.getSize(response)

        # check if all the content has been received
        while True:
            if len(http_response) > required_size - 100:
                break
            else:
                http_response += domain.recv(10000000)
        print(f"received {len(http_response)} size of bytes")
        return http_response

    @staticmethod
    def getDomainAddress_path(path):
        # extract domain name with and without http
        domain_address = path.replace("http://", "").split("/")[0]
        text = f"http://{domain_address}"
        return domain_address, text

    @staticmethod
    def getSize(response):
        # extract content length form the Http Response
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
