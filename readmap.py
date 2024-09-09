import numpy as np 
from headers import *

mapstring = "[0, 0, 0, 1, 0, 0, 0]\n[0, 0, 0, 1, 0, 0, 0]\n[0, 0, 0, 1, 0, 0, 0]\n[1, 1, 1, 0, 1, 1, 1]\n[0, 0, 0, 1, 0, 0, 0]\n[0, 0, 0, 1, 0, 0, 0]\n[0, 0, 0, 1, 0, 0, 0]"
#print(mapstring)

matrix = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
rows = mapstring.split("\n")

for i in range(len(rows)):
    rows[i] = rows[i].replace('[', "").replace(']', "").replace(',', "")
    rows[i] = rows[i].split()

for i in range(len(rows)):
    for j in range(len(rows[i])):
        rows[i][j] = int(rows[i][j])
