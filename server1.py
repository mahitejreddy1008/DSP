import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 65432))
    server_socket.listen()

    print("Server is listening on port 65432...")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Received from client: {data.decode('utf-8')}")
        conn.sendall(data)  # Echo the data back to the client

    conn.close()

if __name__ == "__main__":
    start_server()
