import pymongo

def return_one():
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["recipe_dev"]
  mycol = mydb["Recipe"]

  x = mycol.find_one()

  return x