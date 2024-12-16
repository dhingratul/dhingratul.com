import http.server
import socketserver
import webbrowser
import os
import socket
from pathlib import Path

def find_free_port(start_port=8086, max_attempts=100):
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    raise OSError("Could not find a free port")

# Configuration
PORT = find_free_port()
# Get the root directory (one level up from tests)
ROOT_DIR = Path(__file__).parent.parent.absolute()

# Change directory to the root directory where index.html is located
os.chdir(ROOT_DIR)

print(f"Serving files from: {ROOT_DIR}")

# Set up the server
Handler = http.server.SimpleHTTPRequestHandler
socketserver.TCPServer.allow_reuse_address = True  # Allow port reuse
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server started at http://localhost:{PORT}")
    # Open the default web browser
    webbrowser.open(f'http://localhost:{PORT}')
    # Start the server
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user")