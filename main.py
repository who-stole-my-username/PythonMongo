import pymongo
import curses
from curses import wrapper

def main(stdscr):
  curses.noecho()
  stdscr.keypad(True)
  curses.curs_set(0)
  stdscr.clear()
  stdscr.refresh()
  curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
  COLOR_GREEN = curses.color_pair(1)
  COLOR_ERROR = curses.color_pair(2)
  
  try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["kinofilme"]
    collection = db["dvd_samlung"]
    stdscr.addstr(4, 4, "DVD Samlung Projekt", COLOR_GREEN | curses.A_UNDERLINE)
    stdscr.addstr(8, 4, "1: Daten Abfragen", COLOR_GREEN)
    stdscr.addstr(10, 4, "2: Daten Löschen", COLOR_GREEN)
    stdscr.addstr(12, 4, "3: Daten bearbeiten", COLOR_GREEN)
    
    while True:
      key = stdscr.getkey()
      if key == "1":
        stdscr.clear()
      elif key == "2":
        stdscr.clear()
      elif key == "3":
        stdscr.clear()
      elif key == "4":
        stdscr.clear()


  except Exception:
    stdscr.addstr(4, 4, "Error", COLOR_ERROR)

  finally:
    stdscr.refresh()
    stdscr.getch()
    client.close()

if __name__ == "__main__":
  wrapper(main)
