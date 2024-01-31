import http.server
import socketserver
import subprocess
from urllib.parse import urlparse, parse_qs

HOST = 'localhost'
PORT = 8443

class VulnerableServer(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/vuln':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data_dict = parse_qs(post_data.decode('utf-8'))

            if 'cmd' in post_data_dict:
                cmd = post_data_dict['cmd'][0]
                output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(output.stdout.encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"Missing 'cmd' parameter")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Path not found")

try:
    with socketserver.TCPServer((HOST, PORT), VulnerableServer) as server:
        print(f"Server started at http://{HOST}:{PORT}")
        server.serve_forever()
except Exception as e:
    print(f"Failed to start server: {e}")
