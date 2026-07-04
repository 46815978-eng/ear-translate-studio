import sys
import threading
import subprocess
import time
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

BUILD_DIR = r'C:\Users\Administrator\.qclaw\workspace-x5kuz49xple53hhg\woxueshe\frontend\build\web'
PORT = 8080

def run_server():
    os.chdir(BUILD_DIR)
    server = HTTPServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler)
    print(f'Serving at http://localhost:{PORT}')
    server.serve_forever()

if __name__ == '__main__':
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    print('Flutter Web server started')
    print(f'Open browser: http://localhost:{PORT}')
    input('Press Enter to stop...')
