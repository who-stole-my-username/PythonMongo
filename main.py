import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["kinofilme"]
collection = db["dvd_samlung"]

print("+--------------------------------------------+")
print("|            Was möchten sie tun?            |")
print("+---+----------------++---+------------------+")
print("| 1 | Daten abfragen || 2 | Daten bearbeiten |")
print("+---+----------------++---+------------------+")
choose = input("Auswahl: ")

client.close()
