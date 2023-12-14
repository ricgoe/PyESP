import socket
from usetester import feed_log

client_connection = None

def create_server(port=80):
    global client_connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", port))
    server_socket.listen(1)
    print(f"Serving HTTP on port {port} ...")
    http_response = "empty in here..."
    while True:
        client_connection, client_address = server_socket.accept()
        request = client_connection.recv(1024).decode()
        print(request.splitlines()[0].split()[1][1:]) #DEBUG: test request info
        client_connection.send(b"HTTP/1.1 200 OK\n\n")
        # client_connection.send(b"Content-Type: text/html\n\n")
        if request.splitlines()[0].split()[1][1:] != "":
            try:
                with open(request.splitlines()[0].split()[1][1:]) as f:
                    http_response = f.read()
            except FileNotFoundError:
                http_response = "File not found\n"
        # print(http_response)
        client_connection.sendall(http_response.encode("utf-8"))
        client_connection.close()


if __name__ == "__main__":
    create_server()  # Call the function to start the server
