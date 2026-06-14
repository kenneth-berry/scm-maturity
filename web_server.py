#!/usr/bin/env python3
"""
Simple HTTP server to serve the Berry Consulting Supply Chain Maturity Assessment web application
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import socket
import subprocess
import platform
import time
from pathlib import Path

def is_port_available(port):
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except OSError:
            return False

def get_process_using_port(port):
    """Get the process ID and name using a specific port"""
    try:
        if platform.system() == 'Windows':
            # Use netstat to find the process
            result = subprocess.run(
                ['netstat', '-ano'],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.split('\n'):
                # Look for lines with LISTENING state and matching port
                if 'LISTENING' in line and f':{port}' in line:
                    # Parse the line - format: TCP    0.0.0.0:8000    0.0.0.0:0    LISTENING    12345
                    parts = line.split()
                    # Find the PID (last number in the line)
                    for part in reversed(parts):
                        if part.isdigit():
                            pid = part
                            try:
                                # Get process name
                                proc_result = subprocess.run(
                                    ['tasklist', '/FI', f'PID eq {pid}', '/FO', 'CSV', '/NH'],
                                    capture_output=True,
                                    text=True,
                                    check=True
                                )
                                if proc_result.stdout.strip():
                                    proc_name = proc_result.stdout.split(',')[0].strip('"')
                                    return {'pid': pid, 'name': proc_name}
                                return {'pid': pid, 'name': 'Unknown'}
                            except:
                                return {'pid': pid, 'name': 'Unknown'}
        else:
            # Linux/Mac - use lsof
            result = subprocess.run(
                ['lsof', '-ti', f':{port}'],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0 and result.stdout.strip():
                pid = result.stdout.strip().split('\n')[0]
                try:
                    proc_result = subprocess.run(
                        ['ps', '-p', pid, '-o', 'comm='],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    proc_name = proc_result.stdout.strip()
                    return {'pid': pid, 'name': proc_name}
                except:
                    return {'pid': pid, 'name': 'Unknown'}
    except Exception:
        return None
    return None

def free_port(port):
    """Attempt to free a port by stopping the process using it"""
    process_info = get_process_using_port(port)
    if not process_info:
        return False
    
    pid = process_info['pid']
    name = process_info['name']
    
    try:
        if platform.system() == 'Windows':
            subprocess.run(
                ['taskkill', '/F', '/PID', pid],
                capture_output=True,
                text=True,
                check=True
            )
        else:
            subprocess.run(
                ['kill', '-9', pid],
                capture_output=True,
                text=True,
                check=True
            )
        
        # Wait a moment for the port to be released
        time.sleep(0.5)
        
        # Verify port is now available
        if is_port_available(port):
            return True
    except Exception as e:
        return False
    
    return False

def find_available_port(start_port, max_attempts=20):
    """Find the next available port starting from start_port"""
    for i in range(max_attempts):
        port = start_port + i
        if is_port_available(port):
            return port
    return None

def check_and_prepare_port(port, service_name="Web Server"):
    """Check port availability and prepare it, returning the port to use"""
    if is_port_available(port):
        return port
    
    # Port is in use
    process_info = get_process_using_port(port)
    if process_info:
        pid = process_info['pid']
        name = process_info['name']
        print(f"⚠️  Port {port} is in use for {service_name}")
        print(f"   Process: PID {pid} ({name})")
        print("   Attempting to free port...")
        
        if free_port(port):
            print(f"✅ Successfully freed port {port}")
            return port
        else:
            print(f"   Port {port} cannot be freed. Finding next available port...")
    else:
        print(f"⚠️  Port {port} is in use for {service_name}")
        print("   Finding next available port...")
    
    # Find next available port
    available_port = find_available_port(port, max_attempts=20)
    if available_port:
        print(f"✅ Found available port: {available_port} for {service_name}")
        return available_port
    else:
        print(f"❌ Could not find an available port after {20} attempts")
        return None

def start_server(port=8000):
    """Start a simple HTTP server and open the browser"""
    
    # Check and prepare port (automatic port detection)
    actual_port = check_and_prepare_port(port, "Web Server")
    if actual_port is None:
        print(f"❌ Error: Could not find an available port")
        sys.exit(1)
    
    if actual_port != port:
        print(f"📌 Web Server will use port: {actual_port}")
    
    # Change to the directory containing the HTML file
    web_dir = Path(__file__).parent
    os.chdir(web_dir)
    
    try:
        # Create server
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", actual_port), Handler) as httpd:
            server_url = f"http://localhost:{actual_port}"
            
            print("=" * 60)
            print("🌐 Berry Consulting Supply Chain Maturity Assessment Web Server")
            print("=" * 60)
            print(f"✅ Server started successfully!")
            print(f"📍 URL: {server_url}")
            print(f"📁 Serving files from: {web_dir}")
            print(f"🔌 Port: {actual_port}")
            print()
            print("💡 The web application should open automatically in your browser.")
            print("   If it doesn't, copy the URL above and paste it into your browser.")
            print()
            print("⏹️  Press Ctrl+C to stop the server")
            print("=" * 60)
            
            # Open browser automatically
            try:
                webbrowser.open(server_url)
                print("🚀 Opening browser...")
            except Exception as e:
                print(f"⚠️  Could not open browser automatically: {e}")
                print(f"   Please open {server_url} manually in your browser")
            
            print("\n🎯 Ready to test! The Berry Consulting Supply Chain Maturity Assessment tool is now running in your browser.")
            print("\nFeatures available:")
            print("  • Interactive assessment questionnaire")
            print("  • Real-time progress tracking")
            print("  • Quick demo mode")
            print("  • Detailed results with recommendations")
            print("  • Export results as JSON")
            print("  • Mobile-responsive design")
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
        sys.exit(0)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {actual_port} is already in use.")
            print("💡 This should not happen with automatic port detection.")
            print("   Please check for other processes using this port.")
            sys.exit(1)
        else:
            print(f"❌ Error starting server: {e}")
            sys.exit(1)

if __name__ == "__main__":
    port = 8000
    
    # Check if port is specified as command line argument
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Invalid port number. Using default port 8000.")
    
    start_server(port)