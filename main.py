import pymongo as mdb

client = mdb.MongoClient(
  "mongodb://localhost:27017/"
)

client.close()
