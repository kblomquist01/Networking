import threading
import socket

host = "127.0.0.2"
port = 22222

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
client_names = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try: 
            if(clients.count(client) > 0):
                index = clients.index(client)
                message = client.recv(1024)
                if(index < len(clients) and message.decode("ascii") == f"{client_names[index]}: GAME"):
                    client.send("which user would you like to play with: ".encode("ascii"))
                    invited_name = client.recv(1024).decode("ascii").replace(f"{client_names[index]}: ", "")
                    

                    if(client_names.count(invited_name) != 0):
                        index_invite = client_names.index(invited_name)
                        invited = clients[index_invite]
                        invited.send(f"do you want to play a game with {client_names[index]} (yes/no)".encode("ascii"))
                        message_invite = invited.recv(1024).decode("ascii").replace(f"{invited_name}: ", "")

                        if(message_invite == "yes"):
                            client.send(f"{invited_name} accepted... sending to game lobby".encode("ascii"))
                            invited.send("accepted... sending to game lobby".encode("ascii"))

                            game = Game(client, invited)

                            broadcast(f"{client_names[index]} is playing a game with {invited_name}".encode("ascii"))

                            clients.remove(client)
                            client_name = client_names[index]
                            client_names.remove(client_name)
                            clients.remove(invited)
                            client_names.remove(invited_name)

                            invited.send("NAME".encode("ascii"))

                            game.play()

                            clients.append(client)
                            client_names.append(client_name)
                            clients.append(invited)
                            client_names.append(invited_name)

                            broadcast(f"{client_name} and {invited_name} have rejoined".encode("ascii"))

                        
                    else:
                        client.send("user not found".encode("ascii"))


                else:
                    broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()

            client_name = client_names[index]
            broadcast(f"{client_name} has left".encode("ascii"))
            client_names.remove(client_name)
            break

def recieve():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")

        client.send("NAME".encode("ascii"))
        client_name = client.recv(1024).decode("ascii")

        client_names.append(client_name)
        clients.append(client)

        print(f"client named {client_name}")

        broadcast(f"{client_name} has joined the chat".encode("ascii"))
        client.send("connected to the server".encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

class Game:
    def __init__(self, client1, client2):
        self.player1 = client1
        self.player2 = client2

    def displayBoard(self, board):
        display = f"{board[0]}|{board[1]}|{board[2]}\n"
        display += "-+-+-\n"
        display += f"{board[3]}|{board[4]}|{board[5]}\n"
        display += "-+-+-\n"
        display += f"{board[6]}|{board[7]}|{board[8]}"
        self.player1.send(display.encode("ascii"))
        self.player2.send(display.encode("ascii"))
    
    def turn(self, client, player, board):
            
            client.send("NAME".encode("ascii"))
            client_name = client.recv(1024).decode("ascii")
            test = True
            valid = False

            while(test):
                self.displayBoard(board)
                client.send(f"where do you want to place your {player} (1-9): ".encode("ascii"))
                choice = int(client.recv(1024).decode("ascii").replace(f"{client_name}: ", ""))

                valid = (test and (board[choice - 1] != "o" or board[choice - 1] != "x"))
                if(valid):
                    board[choice - 1] = player
                    test = False
                if(not valid):
                    client.send("Please choose a VALID spot".encode("ascii"))

    def play(self):

        board = [1,2,3,4,5,6,7,8,9]
 
        play = True
        turnNum = 1

        while(play):
            # goes through each players turn then checks if they won

            if(play):
                self.turn(self.player1, "x", board)
                play = self.winCondition(self.player1, board, turnNum)
                turnNum += 1
            if(play):            
                self.turn(self.player2, "y", board)
                play = self.winCondition(self.player2, board, turnNum)
                turnNum += 1
        

    def winCondition(self, client, board, turnNum):
        client.send("NAME".encode("ascii"))
        client_name = client.recv(1024).decode("ascii")
        if(board[0] == board[1] and board[1] == board[2]):
            self.broadcast(client_name)
            return False
        elif(board[3] == board[4] and board[4] == board[5]):
            self.broadcast(client_name)
            return False
        elif(board[6] == board[7] and board[7] == board[8]):
            self.broadcast(client_name)
            return False
        elif(board[0] == board[3] and board[3] == board[6]):
            self.broadcast(client_name)
            return False
        elif(board[1] == board[4] and board[4] == board[7]):
            self.broadcast(client_name)
            return False
        elif(board[2] == board[5] and board[5] == board[8]):
            self.broadcast(client_name)
            return False
        elif(board[0] == board[4] and board[4] == board[8]):
            self.broadcast(client_name)
            return False
        elif(board[2] == board[4] and board[4] == board[6]):
            self.broadcast(client_name)
            return False
        elif(turnNum == 9):
            self.broadcast("no one")
            return False
        return True
        
    def broadcast(self, client):
        self.player1.send(f"{client} won!".encode("ascii"))
        self.player2.send(f"{client} won!".encode("ascii"))

print("server live...")
recieve()


