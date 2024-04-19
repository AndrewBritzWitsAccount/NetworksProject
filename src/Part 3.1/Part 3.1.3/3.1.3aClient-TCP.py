# Import the socket module, which provides access to the BSD socket interface
import socket

# Create a new socket object using IPv4 address family (AF_INET) and TCP protocol (SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the specified host (current machine's hostname) and port 6060
s.connect((socket.gethostname(), 6060))

# Send a message to the server by encoding it as UTF-8 bytes and sending it through the socket
s.send(bytes("Hello from client", "utf-8"))

# Receive data from the connected socket, with a maximum buffer size of 2048 bytes
message = s.recv(2048)

# Print the received message after decoding it from UTF-8 bytes to a string
print(f"Message Received from server: {message.decode('utf-8')}")

# Close the socket
s.close()

