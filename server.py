import http.server
import socketserver
import json
import os
import sys
import socket
import traceback
from urllib.parse import parse_qs, urlparse
from datetime import datetime

# File to store emails
EMAILS_FILE = "emails.json"

# Initialize emails file if it doesn't exist
if not os.path.exists(EMAILS_FILE):
    print(f"Creating new emails file at {os.path.abspath(EMAILS_FILE)}")
    with open(EMAILS_FILE, "w") as f:
        json.dump([], f)
else:
    print(f"Using existing emails file at {os.path.abspath(EMAILS_FILE)}")
    try:
        with open(EMAILS_FILE, 'r') as f:
            emails = json.load(f)
            print(f"Loaded {len(emails)} emails from file")
    except json.JSONDecodeError:
        print(f"WARNING: emails.json exists but contains invalid JSON. Creating backup and starting fresh.")
        os.rename(EMAILS_FILE, f"{EMAILS_FILE}.bak.{int(datetime.now().timestamp())}")
        with open(EMAILS_FILE, "w") as f:
            json.dump([], f)

class EmailHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        """Override to provide more detailed logging"""
        sys.stderr.write(f"[{self.log_date_time_string()}] {self.address_string()} - {format % args}\n")
    
    def do_GET(self):
        self.log_message(f"GET request received: {self.path}")
        
        # Handle API requests
        if self.path == '/api/emails':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Read emails from file
            try:
                self.log_message(f"Reading emails from {EMAILS_FILE}")
                with open(EMAILS_FILE, 'r') as f:
                    emails = json.load(f)
                self.log_message(f"Successfully loaded {len(emails)} emails")
                self.wfile.write(json.dumps(emails).encode())
            except Exception as e:
                error_msg = f"Error reading emails: {str(e)}"
                self.log_message(error_msg)
                self.log_message(traceback.format_exc())
                self.wfile.write(json.dumps({"error": error_msg}).encode())
        else:
            # Serve static files
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        self.log_message(f"POST request received: {self.path}")
        
        # Handle API requests
        if self.path == '/api/emails':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                self.log_message(f"Parsing email data")
                email_data = json.loads(post_data)
                
                # Read existing emails
                self.log_message(f"Reading existing emails")
                with open(EMAILS_FILE, 'r') as f:
                    emails = json.load(f)
                
                # Add new email
                self.log_message(f"Adding new email: {email_data.get('subject', 'No subject')}")
                emails.append(email_data)
                
                # Write back to file
                self.log_message(f"Writing updated emails to file")
                with open(EMAILS_FILE, 'w') as f:
                    json.dump(emails, f)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode())
                self.log_message(f"Email added successfully")
            
            except Exception as e:
                error_msg = f"Error adding email: {str(e)}"
                self.log_message(error_msg)
                self.log_message(traceback.format_exc())
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": error_msg}).encode())
        
        elif self.path == '/api/clear':
            try:
                # Clear all emails
                self.log_message(f"Clearing all emails")
                with open(EMAILS_FILE, 'w') as f:
                    json.dump([], f)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode())
                self.log_message(f"All emails cleared successfully")
            
            except Exception as e:
                error_msg = f"Error clearing emails: {str(e)}"
                self.log_message(error_msg)
                self.log_message(traceback.format_exc())
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": error_msg}).encode())
        else:
            self.log_message(f"Endpoint not found: {self.path}")
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

def find_free_port(start_port=8000, max_attempts=10):
    """Find a free port starting from start_port"""
    print(f"Looking for a free port starting from {start_port}...")
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                print(f"Found free port: {port}")
                return port
        except OSError:
            print(f"Port {port} is in use, trying next...")
            continue
    return None

def get_ip_addresses():
    """Get all IP addresses for the machine"""
    import socket as socket_module  # Rename to avoid conflict
    
    hostname = socket_module.gethostname()
    print(f"Hostname: {hostname}")
    
    # Get all IP addresses
    try:
        # Try to get the primary IP
        primary_ip = socket_module.gethostbyname(hostname)
        print(f"Primary IP: {primary_ip}")
    except:
        primary_ip = "Could not determine"
        print(f"Could not determine primary IP")
    
    # Get all network interfaces
    print("\nAll network interfaces:")
    all_ips = []
    try:
        import netifaces
        for interface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    ip = addr['addr']
                    if ip != '127.0.0.1':
                        all_ips.append(ip)
                        print(f"  - {interface}: {ip}")
    except ImportError:
        print("  netifaces module not installed. For better IP detection, install with: pip install netifaces")
        # Fallback method
        try:
            s = socket_module.socket(socket_module.AF_INET, socket_module.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            all_ips.append(ip)
            print(f"  - Default interface: {ip}")
        except:
            print("  Could not determine IP addresses")
    
    return primary_ip, all_ips

def run_server(port=8000):
    """Run the server on the specified port or find a free one"""
    try:
        print("\n" + "="*50)
        print("STARTING DIGITAL FORTRESS EMAIL SERVER")
        print("="*50)
        
        # Get IP addresses
        primary_ip, all_ips = get_ip_addresses()
        
        # Try the specified port first
        Handler = EmailHandler
        
        # Allow address reuse
        socketserver.TCPServer.allow_reuse_address = True
        
        print(f"\nStarting server on port {port}...")
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print("\n" + "="*50)
            print("SERVER RUNNING SUCCESSFULLY")
            print("="*50)
            print(f"\nLocal access:")
            print(f"  Admin interface: http://localhost:{port}/admin.html")
            print(f"  User interface: http://localhost:{port}/index.html")
            
            print(f"\nNetwork access:")
            if all_ips:
                for ip in all_ips:
                    print(f"  Admin: http://{ip}:{port}/admin.html")
                    print(f"  User: http://{ip}:{port}/index.html")
            else:
                print(f"  Admin: http://{primary_ip}:{port}/admin.html")
                print(f"  User: http://{primary_ip}:{port}/index.html")
            
            print("\nPress Ctrl+C to stop the server")
            print("="*50 + "\n")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"Port {port} is already in use.")
            free_port = find_free_port(port + 1)
            if free_port:
                print(f"Trying alternative port {free_port}...")
                run_server(free_port)
            else:
                print("Could not find a free port. Please close other applications or specify a different port.")
                sys.exit(1)
        else:
            print(f"Error: {e}")
            print(traceback.format_exc())
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    # Get port from command line arguments if provided
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}")
            print("Using default port 8000")
    
    run_server(port) 