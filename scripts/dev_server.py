import http.server
import os
import socketserver
import mimetypes

PORT = 8000
DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class CleanUrlHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        clean = self.path.split('?')[0].split('#')[0].strip('/')
        parts = [p for p in clean.split('/') if p and p not in ('.', '..')]
        disk_path = os.path.join(DIRECTORY, *parts) if parts else os.path.join(DIRECTORY, 'index.html')

        if not os.path.exists(disk_path) and os.path.exists(disk_path + '.html'):
            disk_path += '.html'
        elif os.path.isdir(disk_path):
            idx = os.path.join(disk_path, 'index.html')
            if os.path.exists(idx):
                disk_path = idx

        if not os.path.exists(disk_path) or os.path.isdir(disk_path):
            self.send_error(404, "File Not Found")
            return

        ctype, _ = mimetypes.guess_type(disk_path)
        if disk_path.endswith('.css'):
            ctype = 'text/css'
        elif disk_path.endswith('.js'):
            ctype = 'application/javascript'
        elif not ctype:
            ctype = 'application/octet-stream'

        try:
            with open(disk_path, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, str(e))

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CleanUrlHandler) as httpd:
        print(f"Serving {DIRECTORY} with Clean URLs on http://localhost:{PORT}")
        httpd.serve_forever()
