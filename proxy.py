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
        self.__project_root_directory = os.getcwd()
        self.__directory_browsing_mode = True

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
    def handleClient(self, connection):

        # receive HTTP Request
        http_request = connection.recv(1024).decode('utf-8')

        # Process HTTP Request
        request_method, path, version = self.getRequestLine(http_request)

        # Based on method perform operation
        http_response = self.process_client_request(request_method, path)

        connection.send(http_response)
        connection.close()
        pass

    def process_client_request(self, request_method, path):
        if request_method == "GET":
            if path == "/":
                return self.homePage()
            elif os.path.isdir(path):
                return self.sendDirResponse(path)
            elif os.path.isfile(path):
                return self.sendFileResponse(path)
            else:
                return self.sendErrorStatusCode()

    # Extract request line from HTTP Request
    def getRequestLine(self, http_request):
        # split lines into list
        lines = http_request.splitlines()

        # Extract request line details
        if len(lines) == 0:
            return
        request_line = lines[0].split(" ")
        request_method = request_line[0]
        path = request_line[1]
        if request_line[1] != "/":
            path = self.__project_root_directory + request_line[1]
        version = request_line[2]
        return request_method, path, version

    # Send list of all files in that particular directory
    def sendDirResponse(self, path):
        # Generate HTTP Response
        http_response = "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: 1024\nConnection: Closed\n\n"

        # get all files in that directory
        files = os.listdir(path)
        for file in files:
            file_path = os.path.join(path, file)
            text = file_path.replace(self.__project_root_directory, "")
            http_response += f"<a href = '{text}'>{file}</a>\n<br>\n"

        # Send the generated HTTP Response
        return http_response.encode('utf-8')

    def sendFileResponse(self, path):

        if "bin" in path:
            http_response = self.createDynamic(path)
        else:
            http_response = self.createStatic(path)
        return http_response

    @staticmethod
    def sendErrorStatusCode():
        http_response = "HTTP/1.1 404 NOT FOUND\n\n"
        return http_response.encode('utf-8')

    @staticmethod
    def homePage():
        http_response = "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: 1024\nConnection: Closed\n\n"
        http_response += "<a href = '/www'>www</a><br>"
        http_response += "<a href = '/bin'>bin</a>"
        return http_response.encode('utf-8')

    def createDynamic(self, path):
        import sys
        stdin = sys.stdin.fileno()  # usually 0
        stdout = sys.stdout.fileno()  # usually 1

        parent_stdin, child_stdout = os.pipe()
        child_stdin, parent_stdout = os.pipe()
        pid = os.fork()
        sys.stdout.flush()
        if pid > 0:
            # parent process
            os.close(child_stdout)
            os.close(child_stdin)
            os.dup2(parent_stdin, stdin)
            os.dup2(parent_stdout, stdout)
            return self.dynamicServer()

        elif pid == 0:
            # child process
            os.close(parent_stdin)
            os.close(parent_stdout)
            os.dup2(child_stdin, stdin)
            os.dup2(child_stdout, stdout)
            self.dynamicClient(path)
        pass

    @staticmethod
    def createStatic(path):
        # Read file
        file = open(path, 'rb')
        requested_file = file.read()
        file.close()

        # Generate http response header
        file_name = os.path.basename(path)
        content_type = mimetypes.MimeTypes().guess_type(file_name)[0]
        content_length = len(requested_file)
        # Generate http response and convert it to binary
        http_response = f"HTTP/1.1 200 OK\nContent-Type: {content_type}\nContent-Length: {content_length}\nConnection: Closed\n\n"
        http_response = http_response.encode('utf-8')

        # Combine http header and file content
        response_bytes = http_response + requested_file

        return response_bytes

    @staticmethod
    def dynamicServer():
        data = ""
        for line in sys.stdin.readlines():
            data += line

        content_type = "text/plain"
        content_length = len(data)
        http_response = f"HTTP/1.1 200 OK\nContent-Type: {content_type}\nContent-Length: {content_length}\nConnection: Closed\n\n"
        http_response += data
        return http_response.encode('utf-8')

    @staticmethod
    def dynamicClient(path):
        # Extract file details
        file_name = os.path.basename(path)
        content_type = mimetypes.MimeTypes().guess_type(file_name)[0]

        # check type of file and execute the method
        if content_type is None:
            exec("os.system(file_name)")
        else:
            exec(open(path).read())

        # Kill the child process once execution is done
        pid = os.getpid()
        os.kill(pid, signal.SIGTERM)

        pass


def main():
    # test harness checks for your web server on the localhost and on port 8888
    # do not change the host and port
    # you can change  the HTTPServer object if you are not following OOP
    HTTPServer('127.0.0.1', 8888)


if __name__ == "__main__":
    main()
