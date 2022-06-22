import pymongo
from pymongo import MongoClient

myclient = MongoClient(
    "mongodb+srv://akhoa1107:anhkhoa123@cluster0.ns8gwdm.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]
collection = mydb["mydatabase"]

post = {
    "_id": 0,
    "name": "Khoa"
}

result = collection.find({"name": "Khoa"})

for i in result:
    print(i)
