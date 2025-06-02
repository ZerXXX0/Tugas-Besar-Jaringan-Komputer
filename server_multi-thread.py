import socket
import threading
import os

def handle_client(connection_socket, client_address):
    try:
        # Receives up to 1024 bytes from the client, then decodes it into a string.
        request = connection_socket.recv(1024).decode()
        print(f"[REQUEST from {client_address}] {request}")

        # Parse file name from GET request
        lines = request.splitlines()
        if len(lines) == 0:
            return
        filename = lines[0].split()[1].lstrip('/')

        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                content = f.read()
            header = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            response = header + content
        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>"

        # Sends the full response (header + content or error message) to the client.
        connection_socket.sendall(response)
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        connection_socket.close()

def start_server(host='0.0.0.0', port=8080):
    # Creates a TCP socket using IPv4 (AF_INET) and TCP (SOCK_STREAM).
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[SERVER RUNNING] Listening on {host}:{port}")

    # Difference is here
    
    # Creates a new thread to handle the request.
    # threading.Thread(...): Spawns a new worker thread.
    # .start(): Begins executing handle_client() in parallel.
    # This allows the main thread to immediately return to accept() and handle new clients.
    while True:
        client_socket, addr = server_socket.accept()
        print(f"[NEW CONNECTION] {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == '__main__':
    start_server()
