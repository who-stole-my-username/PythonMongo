import pymongo
import curses
from curses import wrapper

def main(stdscr):
  curses.noecho()
  stdscr.keypad(True)
  curses.curs_set(0)
  stdscr.clear()

  stdscr.addstr(4, 4, "Test")

  stdscr.refresh()

  curses.echo()
  curses.curs_set(1)
  stdscr.keypad(False)
  stdscr.refresh()
  curses.endwin()

if __name__ == "__main__":
  client = pymongo.MongoClient("mongodb://localhost:27017/")
  db = client["kinofilme"]
  collection = db["dvd_samlung"]
  stdscr = curses.initscr()
  main(stdscr)

  client.close()
