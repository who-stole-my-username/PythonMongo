import pymongo
import curses
import re
from curses import wrapper
from curses.textpad import Textbox, rectangle

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
    y, x = stdscr.getmaxyx()
    stdscr.addstr(2, 4, "DVD Samlung Projekt", COLOR_GREEN | curses.A_UNDERLINE)
    stdscr.addstr(4, 4, "Was wollen sie tun?", COLOR_GREEN)
    stdscr.addstr(y - 4, 4, "1: Nach Filmen suchen", COLOR_GREEN)
    stdscr.addstr(y - 4, x - 25, "2: Filme bearbeiten", COLOR_GREEN)
    stdscr.addstr(y - 2, 4, "3: Filme einfügen", COLOR_GREEN)
    stdscr.addstr(y - 2, x - 25, "4: Filme Löschen", COLOR_GREEN)

    for i in range(x):
      stdscr.addstr(y - 6, i, "-", COLOR_GREEN)
      i = i + 1

    while True:
      key = stdscr.getkey()
      if key == "1":
        stdscr.clear()
        y, x = stdscr.getmaxyx()
        stdscr.addstr(2, 4, "Nach Filmen suchen", COLOR_GREEN | curses.A_UNDERLINE)
        stdscr.addstr(4, 4, "Nach welchen Kriterien wollen sie suchen?", COLOR_GREEN)
        stdscr.addstr(y - 8, 4, "1: Titel", COLOR_GREEN)
        stdscr.addstr(y - 8, x - 25, "2: Art", COLOR_GREEN)
        stdscr.addstr(y - 6, 4, "3: Jahr", COLOR_GREEN)
        stdscr.addstr(y - 6, x - 25, "4: Regisseur", COLOR_GREEN)
        stdscr.addstr(y - 4, 4, "5: Schauspieler", COLOR_GREEN)
        stdscr.addstr(y - 4, x - 25, "6: Bewertungen", COLOR_GREEN)
        stdscr.addstr(y - 2, 4, "7: Mindestalter", COLOR_GREEN)
        stdscr.addstr(y - 2, x - 25, "8: Bemerkungen", COLOR_GREEN)
        stdscr.refresh()

        for i in range(x):
          stdscr.addstr(y - 10, i, "-", COLOR_GREEN)
          i = i + 1

        key = 0

        while True:
          keyf = stdscr.getkey()
          if keyf:

            if keyf == "1":
              option = "name"
            elif keyf == "2":
              option = "art"
            elif keyf == "3":
              option = "jahr"
            elif keyf == "4":
              option = "regisseur"
            elif keyf == "5":
              option = "schauspieler"
            elif keyf == "6":
              option = "rating"
            elif keyf == "7":
              option = "min_alter"
            elif keyf == "8":
              option = "bemerkung"

            stdscr.clear()
            stdscr.addstr(2, 4, "Nach Filmen suchen", COLOR_GREEN | curses.A_UNDERLINE)
            stdscr.addstr(5, 5, "1: Suchbegriff:", COLOR_GREEN)
            search = curses.newwin(1, x - 25, 5, 21)
            searchbox = Textbox(search)
            result = curses.newpad(1000, x - 5)
            rectangle(stdscr, 4, 4, 6, x - 4)
            rectangle(stdscr, 8, 4, y - 2, x - 4)
            stdscr.refresh()
            searchbox.edit()
            searchinput = searchbox.gather().replace("\n", "").strip()
            results = collection.find({option: {"$regex": searchinput, "$options": "i"}})

            l = 0

            for i in results:
              resultlist = str(i)

              try:
                result.addstr(l, 1, resultlist, COLOR_GREEN)
                l = l + 4
              except curses.error:
                result.addstr(0, 0, "Error", COLOR_ERROR)

            result.refresh(0, 0, 9, 5, y - 3, x - 5)



      elif key == "2":
        stdscr.clear()
      elif key == "3":
        stdscr.clear()
      elif key == "4":
        stdscr.clear()


  except Exception as e:
    stdscr.addstr(4, 4, "Error:", COLOR_ERROR)
    stdscr.addstr(4, 11, str(e), COLOR_ERROR)

  finally:
    stdscr.refresh()
    stdscr.getch()
    client.close()

if __name__ == "__main__":
  wrapper(main)
