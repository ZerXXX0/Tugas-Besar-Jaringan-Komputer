import socket
import sys

def http_client(server_host, server_port, filename):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect
    client_socket.connect((server_host, int(server_port)))

    # Build and send the HTTP GET request
    request_line = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"
    client_socket.sendall(request_line.encode())

    # Receive the response from the server
    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data

    # Decoding and Closing
    print(response.decode(errors='replace'))
    client_socket.close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python client.py <server_host> <server_port> <filename>")
    else:
        _, host, port, file = sys.argv
        http_client(host, port, file)

