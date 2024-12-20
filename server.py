import socket
import threading
import os

HOST = 'localhost'
PORT = 8080
DOCUMENT_ROOT = './www' #root folder for static files

def handle_request(client_socket):
    try:
        # 1 get request
        request = client_socket.recv(1024)
        if not request:
            return
        request_str = request.decode('utf-8', errors='replace')
        # 2 get headers
        headers_part, _, _ = request_str.partition('\r\n\r\n')

        # 3 split headers to methods
        lines = headers_part.split('\r\n')
        request_line = lines[0]

        method, _, _ = request_line.split(' ', 2)

        # 4 give back response index.html
        if method in ['GET', 'HEAD']:
            with open(os.path.join(DOCUMENT_ROOT, 'index.html'), 'rb') as f:
                content = f.read()
            content_length = len(content)
            response_headers = [
                "HTTP/1.1 200 OK",
                "Content-Type: text/html; charset=utf-8",
                f"Content-Length: {content_length}",
            ]
            response_headers_str = "\r\n".join(response_headers) + "\r\n\r\n"
            client_socket.sendall(response_headers_str.encode('utf-8') + content)
    finally:
        client_socket.close()

def start_server():
    # 1. create sockets
    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 2. bind socket to address and port
    s_tcp.bind((HOST, PORT))
    s_tcp.listen(100)
    # 3. in while loop create threads with function for handle_request
    while True:
        client_socket, addr = s_tcp.accept()
        client_handler = threading.Thread(target=handle_request, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
