"""
Class for handling INET game logic
"""
from headers import *
import random as rng
import numpy as np

class Game():
    def __init__(self, p0, p1):
        self.players = [p0, p1]
        self.map = MAP
        self.dy = 2 # damage item y coord
        self.dx = 2 # x coord
        self.hy = 4 # health item y coord
        self.hx = 4 
        self.py = 0 # power item y coord
        self.px = 0

    # generate new coordinates for health item that dont overlap with anything else
    def generatehealth(self):

        new_hy = rng.randint(1, HEIGHT - 2)
        new_hx = rng.randint(1, WIDTH - 2)
        # check fi item or wall exists here
        # contiously generate new coords if new item spawn collide with a player or wall
        while MAP[new_hy][new_hx] == 1 or (new_hy == self.players[0].y and new_hx == self.players[0].x) or (new_hy == self.players[1].y and new_hx == self.players[1].x) or (new_hy == self.hy and new_hx == self.hx) or (new_hy == self.dx and new_hx == self.dx):
            new_hy = rng.randint(1, HEIGHT - 2)
            new_hx = rng.randint(1, WIDTH - 2)
        self.hy = new_hy
        self.hx = new_hx

    # generate new coordinates for damage item that dont overlap with anything else
    def generatedamage(self):
        new_dy = rng.randint(1, HEIGHT - 2)
        new_dx = rng.randint(1, WIDTH - 2)
        # check if item or wall exists here
        while MAP[new_dy][new_dx] == 1 or (new_dy == self.players[0].y and new_dx == self.players[0].x) or (new_dy == self.players[1].y and new_dx == self.players[1].x) or (new_dy == self.hy and new_dx == self.hx) or (new_dy == self.dx and new_dx == self.dx):
            new_dy = rng.randint(1, HEIGHT - 2)
            new_dx = rng.randint(1, WIDTH - 2)
        self.dy = new_dy
        self.dx = new_dx

    # generate new coordinates for power item that dont overlap with anything else
    def generatepowerup(self):
        new_py = rng.randint(1, HEIGHT - 2)
        new_px = rng.randint(1, WIDTH - 2)
        # check if item or wall exists here
        while MAP[new_py][new_px] == 1 or (new_py == self.players[0].y and new_px == self.players[0].x) or (new_py == self.players[1].y and new_px == self.players[1].x) or (new_py == self.hy and new_px == self.hx) or (new_py == self.dx and new_px == self.dx):
            new_py = rng.randint(1, HEIGHT - 2)
            new_px = rng.randint(1, WIDTH - 2)
        self.py = new_py
        self.px = new_px

    # checks if given command is valid for a player
    def command(self, command, player):
        # command = up, down, left, right
        # check if y and x conflict with dydx or hyhx, or walls

        if player == None: # check item spawns
            pass

        if not self.checkcollision(player, command): # if command does not collide with wall or other player
            if command == "up":
                 # do game logic here
                self.players[player].moveup()
                
            elif command == "down":
                self.players[player].movedown()

            elif command == "left":
                self.players[player].moveleft()

            elif command == "right":
                self.players[player].moveright()

            elif command == "damage":

                if player == 1:
                    self.players[0].healthdown()
                else: 
                    self.players[1].healthdown()
            
            # check if player moved on top of an item pickup
            self.checkdamagepickup(player) # also calls generate item functions
            self.checkhealthpickup(player)
            self.checkpowerpickup(player)

    # check wall collision here
    def checkcollision(self, player, command):

        if command == "up":
            if MAP[self.players[player].y - 1][self.players[player].x]  == 1: # collision with walls first
                # check if player has powerup here
                if self.players[player].power > 0:
                    self.players[player].powerdown()
                    return False
                return True
            # then collision with edges of map
            elif self.players[player].y - 1 <= 0:
                return True
            else:
                if self.players[player].y - 1 == self.players[1 - player].y and self.players[player].x == self.players[1 - player].x: # check collision with other player                                             
                    return True
                
        elif command == "down":
            if MAP[self.players[player].y + 1][self.players[player].x]  == 1: # collision with walls first 
                if self.players[player].power > 0: # if player has powerup, they can go through walls
                    self.players[player].powerdown() # but reduce power by 1 for each step
                    return False
                return True
            elif self.players[player].y + 1 >= HEIGHT - 1:
                return True
            else:
                if self.players[player].y + 1 == self.players[1 - player].y and self.players[player].x == self.players[1 - player].x: # check collision with other player                                             
                    return True

        elif command == "left":
            if MAP[self.players[player].y][self.players[player].x - 1]  == 1: # collision with walls first
                if self.players[player].power > 0:
                    self.players[player].powerdown()
                    return False
                return True
            elif self.players[player].x - 1 <= 0:
                return True
            else:
                if self.players[player].y  == self.players[1 - player].y and self.players[player].x - 1 == self.players[1 - player].x: # check collision with other player                                             
                    return True

        elif command == "right":
            if MAP[self.players[player].y][self.players[player].x + 1]  == 1: # collision with walls first
                if self.players[player].power > 0:
                    self.players[player].powerdown()
                    return False
                return True
            elif self.players[player].x + 1 >= WIDTH:
                return True
            else:
                if self.players[player].y  == self.players[1 - player].y and self.players[player].x + 1 == self.players[1 - player].x: # check collision with other player                                             
                    return True

        return False

    # check if player is on top of health item
    def checkhealthpickup(self, player):
        # health pickups
        if self.players[player].y == self.hy and self.players[player].x == self.hx: # if player coords is on a health pickup
            self.players[player].healthup() # +1 health 
            self.generatehealth()           # generate new health spawn
            return True
        
    # check if player is on top of damage item
    def checkdamagepickup(self, player):        
        # damage pickups
        if self.players[player].y == self.dy and self.players[player].x == self.dx:
            self.players[1 - player].healthdown() # damage other player
            self.generatedamage()                 # generate new damage item spawn
            return True

    # check if player is on top of power item
    def checkpowerpickup(self, player):        
        # damage pickups
        if self.players[player].y == self.py and self.players[player].x == self.px:
            self.players[player].setpower() # damage other player
            self.generatepowerup()            # generate new powerup item spawn
            return True
        
    # reset variables to start values after a game
    def resetgame(self):
        self.players[0].y = P0_START_Y 
        self.players[0].x = P0_START_X 

        self.players[1].y = P1_START_Y 
        self.players[1].x = P1_START_X 

        self.players[0].hp = START_HEALTH
        self.players[1].hp = START_HEALTH

        self.players[0].power = START_POWER
        self.players[1].power = START_POWER

        self.generatehealth()
        self.generatedamage()
        self.generatepowerup()

# create player object to keep track of everything
class Player():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.hp = START_HEALTH
        self.power = START_POWER
        
    def moveup(self):
        self.y -= 1

    def movedown(self):
        self.y += 1

    def moveleft(self):
        self.x -= 1

    def moveright(self):
        self.x += 1

    def healthup(self):
        self.hp += 1

    def healthdown(self):
        self.hp -= 1

    def setpower(self):
        self.power = (self.power + 3) % 10 # max 10
    
    def powerdown(self):
        self.power -= 1
