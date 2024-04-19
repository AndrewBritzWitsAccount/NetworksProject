import socket
import threading

def handle_client(data, address, server_socket):
    try:
        # Print a message indicating that a message has been received from a client
        print(f"Message received from {address}: {data.decode('utf-8')}")

        # Send a welcome message back to the client
        server_socket.sendto(b"Welcome to the server", address)
    except Exception as e:
        print(f"Error handling client {address}: {e}")

def start_server():
    # Create a new socket object using IPv4 address family (AF_INET) and UDP protocol (SOCK_DGRAM)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the current machine's hostname and port 6060
    s.bind((socket.gethostname(), 6060))
    print("Server is listening...")

    while True:
        # Receive data and the address of the client
        data, address = s.recvfrom(2048)

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(data, address, s))
        client_thread.start()

if __name__ == "__main__":
    start_server()
