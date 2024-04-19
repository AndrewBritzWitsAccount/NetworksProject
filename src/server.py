#https://youtu.be/JNzfG7XMYSg?si=pBF94c48SCatU49E

# Import the socket module, which provides access to the BSD socket interface
import socket

# Create a new socket object using IPv4 address family (AF_INET) and TCP protocol (SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the current machine's hostname and port 6060
s.bind((socket.gethostname(), 6060))

# Enable the socket to accept incoming connections, with a backlog queue size of 5
s.listen(5)

# Enter an infinite loop to continuously accept incoming connections
while True:
    # Accept a connection; blocks until a connection is made
    clientSocket, address = s.accept()
    
    # Print a message indicating that a connection has been established
    print(f"Connection established from {address}")
    
    # Send a welcome message to the client by encoding it as UTF-8 bytes
    clientSocket.send(bytes("Welcome to the server", "utf-8"))
    
    # Close the client socket
    clientSocket.close()
