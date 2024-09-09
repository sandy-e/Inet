import curses
from curses import wrapper
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP

curses.initscr()

win = curses.newwin(5, 5)
win.border(0)

win.refresh()

def main(win):
    win.getch()



wrapper(main)