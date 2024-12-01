import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

# Configuration
PORT = 8080
DIRECTORY = Path(__file__).parent

# Create required directories if they don't exist
required_dirs = ['css', 'js', 'images']
for dir_name in required_dirs:
    Path(dir_name).mkdir(exist_ok=True)

# Check if required files exist, create them if they don't
required_files = {
    'index.html': '''<!DOCTYPE html>
<html lang="en">
<!-- Your existing index.html content -->
''',
    'css/style.css': '''/* Your existing CSS content */
''',
    'js/main.js': '''// Your existing JavaScript content */
'''
}

for file_path, content in required_files.items():
    file = Path(file_path)
    if not file.exists():
        file.write_text(content)
        print(f"Created {file_path}")

# Change directory to where the script is located
os.chdir(DIRECTORY)

# Set up the server
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    # Open the default web browser
    webbrowser.open(f'http://localhost:{PORT}')
    # Start the server
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user") 