import http.server
import socketserver
import os

PORT = 8001


def create():
    web_dir = os.path.join(os.path.dirname(__file__), '../static')
    os.chdir(web_dir)
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    print("serving at port:" + str(PORT))
    httpd.serve_forever()


def get_url():
    return 'http://localhost:' + str(PORT)
