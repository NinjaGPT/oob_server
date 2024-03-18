import http.server
import socketserver
import random
import string
import os
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta

HOST = '104.225.xxx.xx' # OOB server's IP address
PORT = 8888             # HTTP port
log_file = 'access.log'

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    active_urls = {}
    url_visitors = {}  # visitors' IP

    def do_GET(self):
        try:
            if self.path == '/geturl':
                self.handle_geturl_request()
            elif self.path[1:7] in self.active_urls:
                self.handle_random_url_request()
            elif self.path == '/checklog':
                self.check_log()
            else:
                self.send_error(404, self.path)
                self.access_log()

        except Exception as e:
            self.send_error(500, f"Internal server error: {e}")

    def access_log(self):
        try:
            if os.path.exists(log_file):
                os.remove(log_file)
            with open(log_file,'w') as file:
                file.write(self.path + ' ' + self.client_address[0] + '\n')
        except Exception as e:
            print(f"{e}")

    def check_log(self):
        try:
            if os.path.exists(log_file):
                with open(log_file,'r') as file:
                    log_line = file.readline()
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f'{log_line}'.encode())
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f'No logging any information.'.encode())

        except Exception as e:
            print(f"{e}")

    def handle_geturl_request(self):
        random_url = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        self.active_urls[random_url] = datetime.now()
        self.url_visitors[random_url] = set()  # init
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(f'http://{HOST}:{PORT}/{random_url}\n'.encode())

    def handle_random_url_request(self):
        if datetime.now() - self.active_urls[self.path[1:7]] > timedelta(hours=1):
            self.send_error(404, "URL expired")
            return

        query_components = parse_qs(urlparse(self.path).query)
        file_name = self.path[1:7] + '.txt'  # add .txt extension

        if 'm' in query_components and query_components['m'][0] == '1':
            self.read_and_send_file_content(file_name)
        else:
            self.record_visitor_ip(file_name)



    def record_visitor_ip(self, file_name):
        visitor_ip = self.client_address[0]
        file_name_without_extension = file_name[:-4]
        if len(self.url_visitors[file_name_without_extension]) < 20 and visitor_ip not in self.url_visitors[file_name_without_extension]:
            self.url_visitors[file_name_without_extension].add(visitor_ip)
            try:
                with open(file_name, 'a') as file:
                    file.write(visitor_ip + '\n')
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"{visitor_ip}\n".encode())
            except IOError:
                self.send_error(500, "Internal server error: Unable to write file")
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"{visitor_ip}\n".encode())




    def read_and_send_file_content(self, file_name):
        if os.path.exists(file_name):
            try:
                with open(file_name, 'r') as file:
                    data = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(data.encode())
            except IOError:
                self.send_error(500, "Internal server error: Unable to read file")
        else:
            self.send_error(404, "File not found")

try:
    handler_object = MyHttpRequestHandler
    my_server = socketserver.TCPServer(("0.0.0.0", PORT), handler_object)

    # Start the server
    print(f"Server started at http://{HOST}:{PORT}")
    print(f"Access to http://{HOST}:{PORT}/geturl to fetch random URL.")
    my_server.serve_forever()
except Exception as e:
    print(f"Failed to start server: {e}")
