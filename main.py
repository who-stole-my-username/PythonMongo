import pymongo
import curses
from curses import wrapper

def main(stdscr):
  curses.noecho()
  stdscr.keypad(True)
  curses.curs_set(0)
  stdscr.clear()

  try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["kinofilme"]
    collection = db["dvd_samlung"]
    stdscr.addstr(4, 4, "Test")

  except Exception:
    stdscr.addstr(4, 4, "Error")

  finally:
    stdscr.refresh()
    stdscr.getch()
    client.close()

if __name__ == "__main__":
  wrapper(main)
