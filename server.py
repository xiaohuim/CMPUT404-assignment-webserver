#  coding: utf-8
import SocketServer, os, mimetypes

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Xiaohui Ma
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    def _gen_response(self, request):

        # add the http version to header, eg: "HTTP/1.1"
        header = request.split( )[2]

        # get the file directory from request and add 'www'
        request_file = request.split( )[1]
        request_file = "www" + request_file

        # get the resolved relative path using the os library
        request_file = os.path.relpath(os.path.abspath(request_file))

        # check if the path is within 'www' folder
        if not request_file.startswith("www"):
            # return 404 response if check fails
            header += " 404 Not Found\r\nConnection: close\r\n\r\n"
            r = "<html><body><p>Error 404: File not found</p></body></html>"
            return header+r

        # check if the path is a directory
        if os.path.isdir(request_file):
            request_file += "/index.html"

        # open the requested file
        try:
            f = open(request_file,'r')
            r = f.read()
            f.close()
            # add the 200 status code and the mimetype
            header += " 200 OK\r\nContent-Type: "
            header += mimetypes.guess_type(request_file)[0] + "\r\n"

        except IOError:
            r = "<html><body><p>Error 404: File not found</p></body></html>"
            # add the 404 status code
            header += " 404 Not Found\r\n"

        # end the header with two new lines and merge header with content
        header += "Connection: close\r\n\r\n"
        r = header + r

        return r

    def handle(self):

        self.data = self.request.recv(1024).strip()
        if self.data != "":
            print ("Got a request of: %s\n" % self.data)
            self.request.sendall(self._gen_response(self.data))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
