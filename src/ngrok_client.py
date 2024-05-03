import socket
import threading
import time

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the client socket to the server
client_socket.connect(("0.tcp.ngrok.io", 13256))

# Function for sending an answer to the server
def send_answer(msg):
    ans = msg.encode("utf-8")
    client_socket.send(ans)

# Receive initial message from server
register_msg = client_socket.recv(1024).decode("utf-8")
print(register_msg)

# Receive username prompt from server and send username
user_name = client_socket.recv(1024).decode("utf-8")
username = input(user_name)
send_answer(username)
# Receive password prompt from server and send password
password = client_socket.recv(1024).decode("utf-8")
password = input(password)
send_answer(password)
password_correctness = client_socket.recv(1024).decode("utf-8")
print(password_correctness)

if password_correctness.strip() == "Password accepted. Please proceed with the game":
    # Receive play/invalid message from server
    play_message = client_socket.recv(1024).decode("utf-8")
    print(play_message)
    
    #Game Start
    Message = client_socket.recv(1024).decode("utf-8")
    command_1 = input(Message)
    send_answer(command_1)


    #Question 1
    Round_1 = client_socket.recv(1024).decode("utf-8")
    print(Round_1)
    message_1 = input("Enter your answer for the question: ")
    send_answer(message_1)
    time.sleep(0.1)
    #Question 1 Score
    score_1 = client_socket.recv(1024).decode("utf-8")
    print(score_1)
    
    #Question 2
    Round_2 = client_socket.recv(1024).decode("utf-8")
    print(Round_2)
    message_2 = input("Enter your answer for the question: ")
    send_answer(message_2)
    time.sleep(0.2)
    #Question 2 Score
    score_2 = client_socket.recv(1024).decode("utf-8")
    print(score_2)

    #Question 3
    Round_3 = client_socket.recv(1024).decode("utf-8")
    print(Round_3)
    message_3 = input("Enter your answer for the question: ")
    send_answer(message_3)
    time.sleep(0.2)
    #Question 3 Score
    score_3 = client_socket.recv(1024).decode("utf-8")
    print(score_3)

    #Question 4
    Round_4 = client_socket.recv(1024).decode("utf-8")
    print(Round_4)
    message_4 = input("Enter your answer for the question: ")
    send_answer(message_4)
    time.sleep(0.2)
    #Question 4 Score
    score_4 = client_socket.recv(1024).decode("utf-8")
    print(score_4)

    # Close the client socket
    client_socket.close()
else:
    print("Access denied due to incorrect password.")


