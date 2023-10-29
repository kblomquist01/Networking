# Overview

{Important!  Do not say in this section that this is college assignment.  Talk about what you are trying to accomplish as a software engineer to further your learning.}

This is a networking program. it uses a client and a server to create a chat function. to use the server just run it and it will go live and start keeping track of who comes in and
who leaves as well as handle all the communication between clients. the client is able to communicate with other clients. they also have the ability to play games with eachother
by using the key GAME and they will then be asked who they want to play with, that user will recieve an invite for if they want to play or not. to connect to the server just run 
the client program and input your prefered nickname.

{Describe your purpose for writing this software.}
The purpose of this software is to create a simple chat function that also allows for multiplayer games between the clients

{Provide a link to your YouTube demonstration.  It should be a 4-5 minute demo of the software running (you will need to show two pieces of software running and communicating with each other) and a walkthrough of the code.}

[Software Demo Video](http://youtube.link.goes.here)

# Network Communication

This is a peer-to-peer network that allows for simple chatting and games


I used TCP and port 22222 for this program

{Identify the format of messages being sent between the client and server or the messages sent between two peers.}
the messages are formatted with their nickname(chosen before joining the server): message
ex: gamer123: hey whats up

# Development Environment

to develope this software I used Socket and Threading imports

I programmed this in python

# Useful Websites

* [https://docs.python.org](https://docs.python.org/3.6/library/socket.html)
* [https://docs.python.org](https://docs.python.org/3.6/library/socketserver.html)

# Future Work

{Make a list of things that you need to fix, improve, and add in the future.}
* error handling for the game, can be improved
* when a game invite is sent the first response goes to the chat and not a response to the invite, can be improved
* when 2 clients send invites to eachother it causes the server to break, needs to be fixed
