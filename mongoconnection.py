import pymongo

def return_one():
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["recipe_dev"]
  mycol = mydb["Recipe"]

  return mycol.find_one()

def mongo_setup():
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["recipe_dev"]
  mycol = mydb["Recipe"]

  return mycol