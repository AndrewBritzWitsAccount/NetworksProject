import socket
import time
import threading

# Define Port and Address
HOST = socket.gethostname()
PORT = 8888

# Create a new socket object using IPv4 address family (AF_INET) and TCP protocol (SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the current machine's hostname and port
server.bind((HOST, PORT))
DISCONNECT = "END"
BEGIN = "START"

# Questions and answers
questions = ['21+42', '133-4', '125x8', '96/2']
answers = [63, 129, 1000, 48]

# Lists for Storing Information
clientsLength = 0
clients = []
clientScoreArray =[0,0]
clientScore =0
clientAnswers = {} 
clientAnswerTime = {}
username = []
password = "mathematics"
# Arrays to store RTTs and time offsets
#rtt_array = [float('nan')] * 1
RTT_Array ={}
time_offsets_array= [0,0]
time_offset =0
#Lists for Storing Information on Answer Times
answer_time_array = []

#Barrier for START
barrier = threading.Barrier(2)

# User Sign In - Game is Password Protected
def signIn(conn, client_ID):
    clients.append((conn, client_ID))
    conn.send(str.encode("Please sign in with your username and the game password to play"))
    time.sleep(0.1)
    conn.send(str.encode("Please enter a username: "))
    name = conn.recv(1024).decode("utf-8")
    username.append(name)
    conn.send(str.encode("Please enter the password: "))
    password_attempt = conn.recv(1024).decode("utf-8")
    # Verify password
    if password_attempt.strip() == "mathematics":
        conn.send(str.encode("Password accepted. Please proceed with the game"))
        return True
    else:
        conn.send(str.encode("Incorrect password. Access denied."))
        return False
    
def handle_client(conn, client_ID):
    if not signIn(conn, client_ID):
        return
    global clients
    print(f"[NEW CONNECTION] {client_ID} connected.")
    clients.append((conn, client_ID))
    conn.send(f"Welcome to the math quiz game server! Waiting for other players to connect...".encode("utf-8"))
    try:
        while True:
            start_time = time.time()
            conn.send(str.encode("To start the game, please type START:"))
            data = conn.recv(1024)
            end_time = time.time()
            rtt = end_time - start_time  # Calculate RTT
            RTT_Array[conn, client_ID] = rtt
            delay = calculate_offset()
            print(f"Delay {delay}")
            barrier.wait()
            for i in range(len(questions)):
                question = questions[i]
                time.sleep(delay) #Calculated Delay
                answer_start_time = time.time()
                conn.send(str.encode(f"Question {i + 1}: {question}"))
                # Receive answer from client
                client_answer = conn.recv(1024).decode("utf-8").strip()
                #Determine Time Taken to Answer
                answer_end_time = time.time()
                answer_rtt = answer_end_time-answer_start_time
                clientAnswerTime[conn, client_ID] = answer_rtt
                #calculate_answer_time()
                
                # Store the answer in the dictionary keyed by the client ID
                clientAnswers[client_ID] = client_answer
                if client_answer == str(answers[i]):
                    conn.send(str.encode("Correct!\n"))
                    if clientsLength == 2:
                        clientScoreArray[1] +=1
                    else:
                        clientScoreArray[0] +=1  
                else:
                    conn.send(str.encode("Incorrect.\n"))
                barrier.wait()
    except ConnectionResetError:
        print(f"Client {client_ID} disconnected.")


def calculate_offset():
    global RTT_Array
    if len(RTT_Array) == 2:
        keys_iterator = iter(RTT_Array.keys())
        rtt1_key = next(keys_iterator)
        rtt2_key = next(keys_iterator)
        rtt1 = RTT_Array[rtt1_key]
        rtt2 = RTT_Array[rtt2_key]
        print(f"RTT1: {rtt1}")
        print(f"RTT2: {rtt2}")

        if rtt1 > rtt2:
            time_offset = abs(rtt1 - rtt2) / 2
            #time_offsets_array = [0, time_offset]
        else:
            time_offset = abs(rtt2 - rtt1) / 2
            #time_offsets_array = [time_offset, 0]

        return time_offset  # Return the calculated time_offset value
    return 0
        

   
# Main loop
def main():
    server.listen()  # Start listening for connections
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    print("Waiting for connection from game clients, server has started ")
    while True:
        conn, client_ID = server.accept()  # Accept incoming connections
        thread = threading.Thread(target=handle_client, args=(conn, client_ID))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")  # Keeping track of client threads


main()
