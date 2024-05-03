import socket
import time
import threading

# Define Port and Address
HOST = socket.gethostname()
PORT = 5555

# Create a new socket object using IPv4 address family (AF_INET) and TCP protocol (SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the current machine's hostname and port
server.bind((HOST, PORT))
DISCONNECT = "END"
BEGIN = "START"

# Lists for Storing Information
clientsLength = 0
clients = []
clientScoreArray =[0,0]
clientScore =0
clientAnswers = {} 
username = []
password = "mathematics"
# Arrays to store RTTs and time offsets
rtt_array = [float('nan')] * 1
time_offsets_array= [0,0]
time_offset =0
#Lists for Storing Information on Answer Times
answer_time_array = []


# Questions and answers
questions = ['21+42', '133-4', '125x8', '96/2']
answers = [63, 129, 1000, 48]

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
    

def calculate_offset():
    global time_offsets_array
    if clientsLength == 2:
        del rtt_array[0]
        print(f"RTT Array: {rtt_array}")
        rtt1 = rtt_array[0];
        rtt2 = rtt_array[1];
        print(f"Rtt1: {rtt1}")
        print(f"RTT2: {rtt2}")

        if rtt1 > rtt2:
            time_offset = abs(rtt1 - rtt2) / 2
            time_offsets_array = [0, time_offset]
        else:
            time_offset = abs(rtt2 - rtt1) / 2
            time_offsets_array = [time_offset, 0]

    return time_offsets_array  # Return the calculated time_offset value


def calculate_answer_time():
    global answer_time_array
    global clientScoreArray
    #del answer_time_array[0]
    #del answer_time_array[1]
    if len(answer_time_array) >=2:
        print(f"Answer Time Array Pre Deletion: {answer_time_array}")
        del answer_time_array[0]
        del answer_time_array[1]
        print(f"Answer Time Array: {answer_time_array}")
        answer1 = answer_time_array[0]
        answer2 = answer_time_array[1]
        print(f"Player 1 Answer Time: {answer1}")
        print(f"Player 2 Answer Time: {answer2}")
        #del answer_time_array[0]
        #del answer_time_array[1]

        if answer2 > answer1:
            clientScoreArray[0] +=1
        else:
            clientScoreArray[1] +=1
    
  

'''
def handle_scores():
    global answer_time_array
    global clientScoreArray
    if answer_time_array[0] < answer_time_array[1]:
        clientScoreArray[0] +=1
    else:
        clientScoreArray[1] +=1
'''
        
def handle_client(conn, client_ID):
    if not signIn(conn, client_ID):
        return
    global clients
    print(f"[NEW CONNECTION] {client_ID} connected.")
    clients.append((conn, client_ID))
    conn.send(f"Welcome to the math quiz game server! Waiting for other players to connect...".encode("utf-8"))
    time.sleep(0.1)
    try:
        while True:
            start_time = time.time()
            conn.send(str.encode("To start the game, please type START:"))
            data = conn.recv(1024)
            end_time = time.time()
            rtt = end_time - start_time  # Calculate RTT
            global clientsLength
            clientsLength +=1
            print(f"No of Clients: {clientsLength}")
            #Determine RTT and Calculate Offset:
            rtt_array.append(rtt)
            offset = calculate_offset()
            print(f"Offset:  {offset}")
            #Determine which player must be delayed:
            if(clientsLength == 2):
                delay = offset[1]
            else:
                delay = offset[0]
            print(f"Delay: {delay}")    
            #Barrier will drop once all players have pressed START
            barrier.wait()
            # Send question to client
            
            #Question 1:
            time.sleep(delay) #Calculated Delay
            conn.send(str.encode(f"Question 1: {questions[0]}"))
            answer_start_time = time.time()
            # Receive answer from client
            client_answer = conn.recv(1024).decode("utf-8").strip()
            answer_end_time = time.time()
            answer_rtt = answer_end_time-answer_start_time
            answer_time_array.append(answer_rtt)
            calculate_answer_time()
            # Store the answer in the dictionary keyed by the client ID
            clientAnswers[client_ID] = client_answer
            if client_answer == str(answers[0]):
                conn.send(str.encode("Correct!\n"))
                if clientsLength == 2:
                    clientScoreArray[1] +=1
                else:
                    clientScoreArray[0] +=1  
            else:
                conn.send(str.encode("Incorrect.\n"))
            barrier.wait()

            #Question 2
            time.sleep(delay) #Calculated Delay
            conn.send(str.encode(f"Question 2: {questions[1]}"))
            answer_start_time = time.time()
            # Receive answer from client
            client_answer = conn.recv(1024).decode("utf-8").strip()
            answer_end_time = time.time()
            answer_rtt = answer_end_time-answer_start_time
            answer_time_array.append(answer_rtt)
            calculate_answer_time()
            # Store the answer in the dictionary keyed by the client ID
            clientAnswers[client_ID] = client_answer
            if client_answer == str(answers[1]):
                conn.send(str.encode("Correct!\n"))
                if clientsLength == 2:
                    clientScoreArray[1] +=1
                else:
                    clientScoreArray[0] +=1  
            else:
                conn.send(str.encode("Incorrect.\n"))
            barrier.wait()




            if(clientScoreArray[0] > clientScoreArray[1]):
                print(f"Player 1 Wins! Score: {clientScoreArray[0]}")
                print(f"Player 2 Score: {clientScoreArray[1]}")
            else:
                print(f"Player 2 Wins! Score: {clientScoreArray[1]}")
                print(f"Player 1 Score: {clientScoreArray[0]}")

    except ConnectionResetError:
        print(f"Client {client_ID} disconnected.")

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

