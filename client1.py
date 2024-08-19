import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 65431))

    message = "Hello, Server!"
    client_socket.sendall(message.encode('utf-8'))

    data = client_socket.recv(1024)
    print(f"Received from server: {data.decode('utf-8')}")

    client_socket.close()

if __name__ == "__main__":
    start_client()
