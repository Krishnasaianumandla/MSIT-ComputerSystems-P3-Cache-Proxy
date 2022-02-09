"""
    Disclaimer
    tiny httpd is a web server program for instructional purposes only
    It is not intended to be used as a production quality web server
    as it does not fully in compliance with the
    HTTP RFC https://tools.ietf.org/html/rfc2616

"""
import mimetypes
import os
import signal
import socket
import sys


class HTTPServer:
    def __init__(self, ip, port):
        self.__IP = ip
        self.__port = port

        # Create server
        self.server = socket.socket()
        self.server_address = (self.__IP, self.__port)
        self.server.bind(self.server_address)

        # Start Server
        self.start()

    # To start server
    def start(self):
        self.server.listen(1)
        print("Server status: online")
        while True:
            connection, client_address = self.server.accept()
            self.handleClient(connection)
        pass

    # Handling client
    @staticmethod
    def handleClient(connection):
        # receive HTTP Request
        http_request = connection.recv(1024).decode('utf-8')

        pass


def main():
    # test harness checks for your web server on the localhost and on port 8888
    # do not change the host and port
    # you can change  the HTTPServer object if you are not following OOP
    HTTPServer('127.0.0.1', 8888)


if __name__ == "__main__":
    main()
