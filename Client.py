import socket
import threading

clientName = input("What is your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.2", 22222))


def recieve():
    while True: 
        try:
            message = client.recv(1024).decode("ascii")

            if message == "NAME":
                client.send(clientName.encode("ascii"))
            else:
                print(message)

        except:
            print("an error has occurred")
            client.close()
            break

def write():
    while True:
        message = clientName + ": " + input()
        client.send(message.encode("ascii"))

threadRecieve = threading.Thread(target=recieve)
threadRecieve.start()

threadWrite = threading.Thread(target=write)
threadWrite.start()