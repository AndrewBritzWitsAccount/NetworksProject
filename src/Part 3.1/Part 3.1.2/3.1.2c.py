import threading
import time

exitFlag = 0

class MyThread(threading.Thread):
    def __init__(self, threadID, name, counter, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.delay = delay

    def run(self):
        print("Starting " + self.name)
        print(self)
        self.print_time()
        print("Exiting " + self.name)

    def print_time(self):
        while self.counter:
            if exitFlag:
                self.name.exit()
            time.sleep(self.delay)
            print("%s: %s %d" % (self.name, time.ctime(time.time()), self.counter))
            print("Thread Name:", threading.currentThread().getName())
            print("Active Threads:", threading.active_count())
            print("Current Thread:", threading.currentThread())

            self.counter -= 1

# Create new threads
threads = []
for i in range(1, 6):
    thread = MyThread(i, "Thread-" + str(i), 10, i)
    threads.append(thread)

# Start new Threads
for thread in threads:
    thread.start()

print("Exiting Main Thread" + '\n')
