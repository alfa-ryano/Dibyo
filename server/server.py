from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import cgi
import urlparse
import ConfigParser

PORT_NUMBER = 8888

class ServerHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == "/post":
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            data = None
            if ctype == 'multipart/form-data':
                data = cgi.parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers.getheader('content-length'))
                data  = urlparse.parse_qs(self.rfile.read(length), keep_blank_values=1)

            subject = data["subject"][0]
            preferenceSheet = data["data"][0]

            filename = subject + ".csv"
            path = os.path.abspath("../ftp/" + filename)
            file = open(path,"w")
            file.write(preferenceSheet)
            file.close()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write("1")

        return

    def do_GET(self):
        if self.path == "/":
            self.path = "index.html"

            sendReply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True

            if sendReply == True:
                fullPath = os.path.abspath(self.path)
                f = open(fullPath)

                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()

                self.wfile.write(f.read())
                f.close()

        elif self.path == "/check":
            config = ConfigParser.ConfigParser()
            config.read("server.ini")
            value = config.getint("Config", "Locked")

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(value)

        return

try:
    server = HTTPServer(('', PORT_NUMBER), ServerHandler)
    print "Started HTTP Server on port", PORT_NUMBER

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print "Shutting down the web server"
    server.socket.close()
