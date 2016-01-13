#  coding: utf-8 
import SocketServer

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
        
        # get the complete file directory
        request_file = request.split( )[1]
        if request_file == "/":
            request_file = "/index.html"
        request_file = "www" + request_file
        
        # add the http version to header, eg: "HTTP/1.1"
        header = request.split( )[2]
        
        # load the requested file
        try:
            f = open(request_file,'r')
            r = f.read()
            f.close()
            # add the 200 status code
            header += " 200 OK\n"
            
            if request_file.endswith(".css"):
                header += "Content-Type: text/css\n"
            
        except Exception as e:
            print ("[Warning!] File not found. Respond with 404 page.\n")
            r = "<html><body><p>Error 404: File not found</p></body></html>"
            # add the 404 status code
            header += " 404 Not Found\n"

        # end the header with two new lines and merge header with content
        header += "Connection: close\n\n"
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
