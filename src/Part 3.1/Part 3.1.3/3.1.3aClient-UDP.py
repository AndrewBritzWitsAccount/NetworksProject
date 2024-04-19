# Import the socket module
import socket

# Create a new socket object using IPv4 address family (AF_INET) and UDP protocol (SOCK_DGRAM)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Specify the server's hostname and port
server_address = (socket.gethostname(), 6060)

# Send data to the server
message = "Hello, server!"
s.sendto(message.encode('utf-8'), server_address)

# Receive data from the server
data, server = s.recvfrom(2048)

# Print the received message after decoding it from UTF-8 bytes to a string
print(f"Message Received: {data.decode('utf-8')}")

# Close the socket
s.close()
