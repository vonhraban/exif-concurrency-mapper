import http.server
import socketserver
import os

PORT = 8001


class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    """This handler uses server.base_path instead of always using os.getcwd()"""
    def translate_path(self, path):
        path = http.server.SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        return os.path.join(self.server.base_path, relpath)


class HTTPServer(http.server.HTTPServer):
    """The main server, you pass in base_path which is the path you want to serve requests from"""
    def __init__(self, base_path, server_address):
        self.base_path = base_path
        http.server.HTTPServer.__init__(self, server_address=server_address, RequestHandlerClass=HTTPHandler)


def create():
    httpd = HTTPServer('./static', ("", PORT))
    print("serving at port:" + str(PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


def get_url():
    return 'http://localhost:' + str(PORT)
