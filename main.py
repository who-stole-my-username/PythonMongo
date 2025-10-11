import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["kinofilme"]
collection = db["dvd_samlung"]

print("+--------------------------------------------+")
print("|            Was möchten sie tun?            |")
print("+---+----------------++---+------------------+")
print("| 1 | Daten abfragen || 2 | Daten bearbeiten |")
print("+---+----------------++---+------------------+")

while True:
  choose = input("Auswahl: ")

  if choose == "1":
    print("1")
  elif choose == "2":
    print("2")
  elif choose == "^C":
    exit
  else:
    print("Keine gültige Auswahl!")

client.close()
