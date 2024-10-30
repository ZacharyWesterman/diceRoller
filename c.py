import curses
from curses import wrapper
from time import sleep

def main(stdscr):
  stdscr.clear()
  stdscr.addstr(0, 0, "hello world")
  stdscr.refresh()
  stdscr.getch()

wrapper(main)
