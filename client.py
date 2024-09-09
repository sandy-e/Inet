import socket
import curses
from curses import wrapper
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP # 261, 260, 258, 259

from headers import *

# connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ipv4, tcp
client.connect(ADDR)
#client.setblocking(0) # enable non-blocking recv
print("Connected to server")

# we recieve info about both players
# format: "y1,x1,y2,x2" --> [(y1,x1) (y2,x2)]
# selfy,selfx,enemyy,enemyx,selflife,enemylife,damagey,damagex,lifeupy,lifeupx#
def read_data(data, olddata):
    try:
        data = data.split(',')
        #p1 = (int(data[0]), int(data[1]))
        #p2 = (int(data[2]), int(data[3]))
        #selflife = data[4]
        #enemylife = data[5]

        return [int(i) for i in data]
    except Exception as e:
        print("read_data ERROR: ", e)
        return olddata
    
    #return [p1, p2, selflife, enemylife]

# exit curses
def exit(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    client.close()
    quit()

def initcurses():
    # curses window
    curses.initscr()
    #stdscr = curses.newwin(HEIGHT, WIDTH)
    curses.start_color()
    # curses color pairs
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    stdscr = curses.newwin(HEIGHT, WIDTH + 1)
    stdscr.clear()
    curses.noecho() # turn off automatic echoing of keys
    curses.cbreak() # react to keys instantly
    stdscr.keypad(True) # to use arrow keys
    curses.curs_set(0) # hide cursor
    stdscr.timeout(10) # timeout to not block forever waiting for player input

    stdscr.addstr(HEIGHT//2, WIDTH//2, "Waiting for player 2...")
    stdscr.refresh()
    return stdscr

def initrender(stdscr, pos):

    # display players
    stdscr.addstr(pos[0], pos[1], "o")
    stdscr.addstr(pos[2], pos[3], "o")
    # display health
    stdscr.addstr(0, 1, f"Life: {pos[4]}  ", curses.color_pair(1))
    stdscr.addstr(0, 10, f"Enemy life: {pos[5]}", curses.color_pair(2))
    
    # draw map
    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if MAP[y][x] == 1:
                stdscr.addch(y, x, '#')

    # draw border
    stdscr.border() 

    # draw damage item
    stdscr.addstr(pos[6], pos[7], "¤")
    # draw health item
    stdscr.addstr(pos[8], pos[9], "*")
    # draw powerup item
    stdscr.addstr(pos[10], pos[11], "+")

    pass

def rerender(stdscr, pos, oldpos):

    GREEN = curses.color_pair(1)
    RED = curses.color_pair(2)
    
    # delete old player pos
    stdscr.addch(oldpos[0], oldpos[1], ' ')
    stdscr.addch(oldpos[2], oldpos[3], ' ')

    # redraw walls if player has moved on top of them
    if MAP[oldpos[0]][oldpos[1]] == 1:
        stdscr.addch(oldpos[0], oldpos[1], '#')
    if MAP[oldpos[2]][oldpos[3]] == 1:
        stdscr.addch(oldpos[2], oldpos[3], '#')

    # refresh player positions
    stdscr.addstr(pos[0], pos[1], "o", GREEN)
    stdscr.addstr(pos[2], pos[3], "o", RED)

    # refresh lives
    stdscr.addstr(0, 1, f"Life: {pos[4]}  ", GREEN)
    stdscr.addstr(0, 10, f"Enemy life: {pos[5]}", RED)

    # refresh powers
    stdscr.addstr(0, 25, f"Powerup: {pos[12]}  ", GREEN)
    stdscr.addstr(0, 37, f"Enemy Powerup: {pos[13]}", RED)

    # delete old player pos
    stdscr.addch(oldpos[6], oldpos[7], ' ')
    stdscr.addch(oldpos[8], oldpos[9], ' ')

    # refresh item pos
    stdscr.addstr(pos[6], pos[7], "¤")
    stdscr.addstr(pos[8], pos[9], "*")
    stdscr.addstr(pos[10], pos[11], "+")

def checkplayerlives(stdscr, pos):

    if(pos[5] < 0): # if opponent disconnects, their life is  sent as -1
        stdscr.erase()
        stdscr.addstr(HEIGHT//2, WIDTH//2, "You Win!")
        stdscr.addstr(HEIGHT//2 + 1, WIDTH//2 - 5, "Opponent disconnected.")
        stdscr.addstr(HEIGHT//2 + 2, WIDTH//2 - 5, "Press space to exit")
        while True:
            k = stdscr.getch() # press space to exit
            if k == 32:
                print(f"enemy hp {pos[5]}")
                exit(stdscr)

    elif (pos[4] == 0): # lose
        stdscr.erase()
        stdscr.addstr(HEIGHT//2, WIDTH//2, "You Lose!")
        stdscr.addstr(HEIGHT//2 + 1, WIDTH//2 - 5, "Press space to exit")
        while True:
            k = stdscr.getch() # press space to exit
            if k == 32:
                exit(stdscr)

    elif (pos[5] == 0): # win
        stdscr.erase()
        stdscr.addstr(HEIGHT//2, WIDTH//2, "You Win!")
        stdscr.addstr(HEIGHT//2 + 1, WIDTH//2 - 5, "Press space to exit")
        while True:
            k = stdscr.getch()
            if k == 32:
                exit(stdscr)

    pass

# sending command and receiving player positions
def send(command):
    client.send(command.encode())
    msg_received = client.recv(128).decode()
    return msg_received


# initilaize connection and curses, then main game loop
def main():
    stdscr = initcurses()

    # receive starting positions of players and items when we first connect
    pos = read_data(client.recv(128).decode(), None)
    oldpos = pos # copy items for deleting old positions on sreen
    stdscr.clear()

    initrender(stdscr, pos) # render everythng including things that dont need rerendering 

    #client.recv(256).decode() # Blocking recv, for debugging

    while True:
        
        # checking enemy and player health
        # if enemy health == 0, player wins
        # if player health == 0, enemy wins
        # after this, server stop sending packets

        checkplayerlives(stdscr, pos)

        command = ""
        c = stdscr.getch() # blocking, timeout 10 ms atm 
        if c == KEY_UP:
            # send in socket to server
            command = "up"
            pass
        elif c == KEY_DOWN:
            command = "down"
            pass
        elif c == KEY_LEFT:
            command = "left"
            pass
        elif c == KEY_RIGHT:
            command = "right"
            pass
        else:
            command = "none"
            #send('0') # maintain connection and to not let server block while waiting for data

        try:
            pos = read_data(send(command), oldpos) # send old data incase we receive faulty data
        except socket.error as e:
            print("error, disconnected: ", e)
            break

        rerender(stdscr, pos, oldpos)    # rerender

        oldpos = pos # save locations for next game loop

        # refresh window after everything has been redrawn
        stdscr.refresh()
        
main()