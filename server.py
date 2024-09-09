import socket
import threading
from game import *
import time
import sys 

from headers import *


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # inet = ipv4, stream = TCP
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reusable
server.bind(ADDR) # bind socket to address and port
server.listen(2) # max two clients 

p0 = Player(P0_START_Y, P0_START_X)
p1 = Player(P1_START_Y, P1_START_X)
game = Game(p0, p1)

"""
Format:
selfy,selfx,enemyy,enemyx,selflife,enemylife,damagey,damagex,lifeupy,lifeupx,powerupy,powerupx,selfpower,enemypower
""" # format gamestate to a string for the player to be sent
def make_data(player):
    return f"{game.players[player].y},{game.players[player].x},{game.players[1 - player].y},{game.players[1 - player].x},{game.players[player].hp},{game.players[1 - player].hp},{game.dy},{game.dx},{game.hy},{game.hx},{game.py},{game.px},{game.players[player].power},{game.players[1-player].power}"


# function for handling a client connection, runs on a thread
def handle_client(conn, addr, player):
    print(f"[CONNECTIONS] New connection: {addr}")
    # send initial positions instanly when we connect
    send(conn, make_data(player), player)

    connected = True
    #msg_length = conn.recv(HEADER).decode(FORMAT) # first message is null, consume it
    while connected: # wait for client to send data

        # check if game over or someone disconnected (-1 hp)
        if(game.players[0].hp <= 0 or game.players[1].hp <= 0):
            print(f"thread {player} exiting")
            sys.exit() # close the thread since we we will start new ones for the next game

        msg = None
        #msg_length = conn.recv(HEADER).decode(FORMAT) # blocking, receive header bytes, utf-8
        try:
            msg = conn.recv(8).decode() # recieve command
            # then send player positions
        except socket.error as error:
            print("ERROR: ", error)
            pass

        game.command(msg, player) # send the command received to the game 

        try: 
            send(conn, make_data(player), player)
            #print("sent info")
        except socket.error as e:
            #print("ERROR: ", e)
            pass

    conn.close() # close connection to client



# main server loop, never exits
def start():
    server.listen() # start listen to connections
    print(f"[LISTENING] Server listening on {SERVER}:{PORT}")
    currentPlayer = 0

    while True:
        game.resetgame()
        conn, addr = server.accept()
        print("Connected to:", addr)
        print("Waiting for player 2")
        while True:
            conn2, addr2 = server.accept()
            print("Connected to:", addr)
            break
        thread1 = threading.Thread(target = handle_client, args = (conn, addr, currentPlayer))
        currentPlayer += 1
        thread2 = threading.Thread(target = handle_client, args = (conn2, addr2, currentPlayer))
        thread1.start()
        thread2.start()

        while thread1.is_alive() and thread2.is_alive():
            time.sleep(0.3) # sleep while main threads are running and to wait for starting new threads after they have finished
        # reset values if playing new game
        currentPlayer = 0
        game.resetgame()


# encodes and sends a text message via socket provided as argument
def send(conn, msg, player):
    message = msg.encode()
    try:
        conn.send(message)
    except: # will pretty much only fail if client has disconnected (or closed game)
        if(game.players[0].hp > 0 and game.players[1].hp > 0):
            game.players[player].hp = -1
            print(f"Player {player} has disconnected. Aborting game, player {1-player} wins." )
            exit(0)

    #msg_received = client.recv(2048).decode(FORMAT)

# start server handler
print("[STARTING] Starting server...")
start()
