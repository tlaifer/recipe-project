def mongo_setup():
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["recipe_dev"]
  mycol = mydb["Recipe"]

  return mycol

import pymongo
from bson.code import Code

mapper = Code("function() { this.ingredients.forEach(function(ingredient) { emit(ingredient, 1); }); }")
reducer = Code("function(key, values) { var total = values.length; return total; }")

db = mongo_setup()
ingredients = []
result = db.map_reduce(mapper, reducer, "results")
for doc in result.find().sort('value', -1).limit(200):
  print(doc)
  ingredients.append(doc['_id'])

'''
 This is needed to add escape char for ingredients like: 
 confectioners' sugar --> confectioners'' sugar
'''
def insert_char(string, index, char):
    return string[:index] + char + string[index:]
    
for x in ingredients:
  if "'" in x:
    x = insert_char(x, x.index("'") , "'")


'''
 Update PG rows
'''
def pg_conn():
    try:
        pg_conn = psycopg2.connect(dbname="recipe_dev", user="postgres", password="postgres")
    except:
        print("Unable to connect to the database.")
    return pg_conn

import psycopg2
conn = pg_conn()
conn.cursor().execute("UPDATE ingredients SET common = false;")
conn.cursor().execute('UPDATE ingredients SET common = true WHERE ingredientname in %(arg)s ;', {
  'arg': tuple(ingredients),
})
conn.commit()  
