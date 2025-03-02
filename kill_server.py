#!/usr/bin/env python3
"""
Script to kill processes using port 8000 (or a specified port)
"""

import os
import sys
import subprocess
import platform

def kill_process_on_port(port=8000):
    """Kill the process using the specified port"""
    system = platform.system()
    
    try:
        if system == "Darwin" or system == "Linux":  # macOS or Linux
            # Find the process ID using the port
            cmd = f"lsof -i :{port} -t"
            result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
            
            if result:
                pids = result.split('\n')
                for pid in pids:
                    print(f"Killing process {pid} using port {port}")
                    os.system(f"kill -9 {pid}")
                print(f"Successfully killed processes using port {port}")
            else:
                print(f"No process found using port {port}")
                
        elif system == "Windows":
            # Find the process ID using the port on Windows
            cmd = f"netstat -ano | findstr :{port}"
            result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
            
            if result:
                lines = result.split('\n')
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[4]
                        print(f"Killing process {pid} using port {port}")
                        os.system(f"taskkill /F /PID {pid}")
                print(f"Successfully killed processes using port {port}")
            else:
                print(f"No process found using port {port}")
        else:
            print(f"Unsupported operating system: {system}")
            return False
            
        return True
    except Exception as e:
        print(f"Error killing process: {e}")
        return False

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}")
            print("Using default port 8000")
    
    kill_process_on_port(port) 