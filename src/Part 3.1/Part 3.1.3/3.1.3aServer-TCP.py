import socket
import threading


def handle_client(clientSocket, address):
    while True:
        try:
            # Receive data from the client
            data = clientSocket.recv(2048).decode('utf-8')
            if not data:
                print(f"Connection closed from {address}")
                break
            
            # Print the data received from the client
            print(f"Received from client {address}: {data}")
            
            # Echo back the received data to the client
            clientSocket.send(bytes(data, 'utf-8'))
        except Exception as e:
            print(f"Error handling client {address}: {e}")
            break
        
    # Close the client socket
    clientSocket.close()

def start_server():
    # Create a new socket object using IPv4 address family (AF_INET) and TCP protocol (SOCK_STREAM)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the current machine's hostname and port 6060
    s.bind((socket.gethostname(), 6060))

    # Enable the socket to accept incoming connections, with a backlog queue size of 5
    s.listen(5)
    print("Server is listening...")

    while True:
        # Accept a connection; blocks until a connection is made
        clientSocket, address = s.accept()
        
        # Print a message indicating that a connection has been established
        print(f"Connection established from {address}")
        
        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(clientSocket, address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
