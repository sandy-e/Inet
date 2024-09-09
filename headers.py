PORT = 5055
SERVER = "localhost" # local WSL ipv4: 127.0.1.1
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

"""
Game constants
"""
HEIGHT = 30
WIDTH = 60
P0_START_Y = 3
P0_START_X = 3
P1_START_Y = 11
P1_START_X = 11
START_HEALTH = 2
START_POWER = 2
POWER_PICKUP = 3
WALL_LENGTH = 12
MAP = [[0 for _ in range(WIDTH + 1)] for _ in range(HEIGHT)]


### generating walls for map
# horizontal lines
#print("row: ", HEIGHT/2)

row = HEIGHT//2 # row in middle of map
for i in range(1, WALL_LENGTH):
    MAP[row][i] = 1 #left wall rightwards
for i in range(WIDTH - WALL_LENGTH, WIDTH):
    MAP[row][i] = 1

column = WIDTH//2 # column in middle of map
for i in range(1, WALL_LENGTH):
    MAP[i][column] = 1
for i in range(HEIGHT - WALL_LENGTH, HEIGHT):
    MAP[i][column] = 1

#print(MAP)
