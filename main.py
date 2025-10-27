import pymongo
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

def dmain(stdscr, COLOR_GREEN):
    stdscr.clear()
    y, x = stdscr.getmaxyx()
    stdscr.addstr(2, 4, "DVD Sammlung", COLOR_GREEN | curses.A_UNDERLINE)
    stdscr.addstr(4, 4, "Was wollen sie tun?", COLOR_GREEN)
    stdscr.addstr(y - 8, 4, "Q: Zurück -> funktioniert immer", COLOR_GREEN | curses.A_DIM)
    stdscr.addstr(y - 4, 4, "1: Nach Filmen suchen", COLOR_GREEN)
    stdscr.addstr(y - 4, x - 25, "2: Filme bearbeiten", COLOR_GREEN)
    stdscr.addstr(y - 2, 4, "3: Filme einfügen", COLOR_GREEN)
    stdscr.addstr(y - 2, x - 25, "4: Filme Löschen", COLOR_GREEN)

    for i in range(x):
      stdscr.addstr(y - 6, i, "-", COLOR_GREEN)
      i = i + 1

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

  state = "main"

  try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["kinofilme"]
    collection = db["dvd_sammlung"]

    dmain(stdscr, COLOR_GREEN)

    while True:
      key = stdscr.getkey()

      if key.lower() == "q":
        if state == "main":
          break
        state = "main"
        dmain(stdscr, COLOR_GREEN)
        continue

      if state == "main":
        if key == "1":
          state = "suchen"
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

        elif key == "2":
          state = "bearbeiten"
          stdscr.clear()
          y, x = stdscr.getmaxyx()
          stdscr.addstr(2, 4, "Filme bearbeiten", COLOR_GREEN | curses.A_UNDERLINE)
          stdscr.addstr(4, 4, "Was wollen sie bearbeiten?", COLOR_GREEN)
          stdscr.addstr(y - 8, 4, "1: Titel", COLOR_GREEN)
          stdscr.addstr(y - 8, x - 25, "2: Art", COLOR_GREEN)
          stdscr.addstr(y - 6, 4, "3: Jahr", COLOR_GREEN)
          stdscr.addstr(y - 6, x - 25, "4: Regisseur", COLOR_GREEN)
          stdscr.addstr(y - 4, 4, "5: Schauspieler", COLOR_GREEN)
          stdscr.addstr(y - 4, x - 25, "6: Bewertungen", COLOR_GREEN)
          stdscr.addstr(y - 2, 4, "7: Mindestalter", COLOR_GREEN)
          stdscr.addstr(y - 2, x - 25, "8: Bemerkungen", COLOR_GREEN)

          for i in range(x):
            stdscr.addstr(y - 10, i, "-", COLOR_GREEN)
            i = i + 1

        elif key == "3":
          state = "einfügen"
          stdscr.clear()
        elif key == "4":
          state = "löschen"
          stdscr.clear()

      elif state == "suchen":
        if key == "1":
          option = "name"
        elif key == "2":
          option = "art"
        elif key == "3":
          option = "jahr"
        elif key == "4":
          option = "regisseur"
        elif key == "5":
          option = "schauspieler"
        elif key == "6":
          option = "rating"
        elif key == "7":
          option = "min_alter"
        elif key == "8":
          option = "bemerkung"

        if option:
          stdscr.clear()
          stdscr.addstr(2, 4, "Nach Filmen suchen", COLOR_GREEN | curses.A_UNDERLINE)
          stdscr.addstr(5, 5, "1: Suchbegriff:", COLOR_GREEN)
          stdscr.addstr(2, 24, option, COLOR_GREEN | curses.A_DIM)
          search = curses.newwin(1, x - 25, 5, 21)
          searchbox = Textbox(search)
          result = curses.newpad(10000, x - 7)
          rectangle(stdscr, 4, 4, 6, x - 4)
          rectangle(stdscr, 8, 4, y - 2, x - 4)
          stdscr.refresh()
          searchbox.edit()
          searchinput = searchbox.gather().replace("\n", "").strip()

          if option == "rating":
            try:
              searchinputfloat = float(searchinput)
              results = collection.find({option: searchinputfloat})
            except ValueError:
              result.addstr(0, 0, "Error, keine gültige Zahl!", COLOR_ERROR)
          elif option in ["jahr", "min_alter"]:
            try:
              searchinputnum = int(searchinput)
              results = collection.find({option: searchinputnum})
            except ValueError:
              result.addstr(0, 0, "Error, keine gültige Zahl!", COLOR_ERROR)
          else:
            results = collection.find({option: {"$regex": searchinput, "$options": "i"}})

          l = 0

          for i in results:
            resultlist = str(i)

            try:
              result.addstr(l, 1, resultlist, COLOR_GREEN)
              l = l + 4
            except curses.error:
              result.addstr(0, 0, "Error", COLOR_ERROR)

          result.refresh(0, 0, 9, 5, y - 3, x - 7)

      elif state == "bearbeiten":
        if key == "1":
          option = "name"
        elif key == "2":
          option = "art"
        elif key == "3":
          option = "jahr"
        elif key == "4":
          option = "regisseur"
        elif key == "5":
          option = "schauspieler"
        elif key == "6":
          option = "rating"
        elif key == "7":
          option = "min_alter"
        elif key == "8":
          option = "bemerkung"

        if option:
          stdscr.clear()
          stdscr.addstr(2, 4, "Filme bearbeiten", COLOR_GREEN | curses.A_UNDERLINE)
          stdscr.addstr(5, 5, "1: Filmtitel des zu bearbeitenden Filmes:", COLOR_GREEN)
          stdscr.addstr(9, 5, f"2: Neue(n/s) {option} eingeben:", COLOR_GREEN)
          stdscr.addstr(2, 24, option, COLOR_GREEN | curses.A_DIM)
          search = curses.newwin(1, x - 51, 5, 47)
          edit = curses.newwin(1, x - 46, 9, 41)
          searchbox = Textbox(search)
          editbox = Textbox(edit)
          rectangle(stdscr, 4, 4, 6, x - 4)
          rectangle(stdscr, 8, 4, 10, x - 4)
          stdscr.refresh()
          searchbox.edit()
          editbox.edit()
          searchinput = searchbox.gather().replace("\n", "").strip()
          editinput = editbox.gather().replace("\n", "").strip()

          film = collection.find_one({"name": {"$regex": searchinput, "$options": "i"}})

          if not film:
            stdscr.addstr(12, 4, "Film nicht gefunden!", COLOR_ERROR)
          else:
            if option == "rating":
              try:
                editinputfloat = float(editinput)
                collection.update_one({"_id": film["_id"]}, {"$set": {option: editinputfloat}})
                stdscr.addstr(12, 4, " Film aktualisiert!", COLOR_GREEN)
              except ValueError:
                stdscr.addstr(12, 4, "Error, keine gültige Zahl!", COLOR_ERROR)
            elif option in ["jahr", "min_alter"]:
              try:
                editinputnum = int(editinput)
                collection.update_one({"_id": film["_id"]}, {"$set": {option: editinputnum}})
                stdscr.addstr(12, 4, " Film aktualisiert!", COLOR_GREEN)
              except ValueError:
                stdscr.addstr(12, 4, "Error, keine gültige Zahl!", COLOR_ERROR)
            elif option in ["art", "schauspieler"]:
              collection.update_one({"_id": film["_id"]}, {"$set": {option: [editinput]}})
              stdscr.addstr(12, 4, " Film aktualisiert!", COLOR_GREEN)
            else:
              collection.update_one({"_id": film["_id"]}, {"$set": {option: editinput}})
              stdscr.addstr(12, 4, " Film aktualisiert!", COLOR_GREEN)

  except Exception as e:
    stdscr.addstr(4, 4, "Error:", COLOR_ERROR)
    stdscr.addstr(4, 11, str(e), COLOR_ERROR)

  finally:
    stdscr.refresh()
    stdscr.getch()
    client.close()

if __name__ == "__main__":
  wrapper(main)
