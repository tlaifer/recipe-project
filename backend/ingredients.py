from .pgconnection import pg_setup
from flask import jsonify
from flask_restful import fields, marshal_with, reqparse, Resource

pgCur = pg_setup()

def getIngredients():

    ingredients = []
    queryString = """SELECT DISTINCT ingredientName FROM ingredients ORDER BY ingredientName"""

    try:
        pgCur.execute(queryString)
    except:
        print("Can't retrieve ingredients.")
        return ingredients

    rows = pgCur.fetchall()
    if (len(rows) > 0):
        for row in rows:
            ingredients.append({ 'name': row[0], 'value': False })

    return ingredients

class IngredientsAPI(Resource):
    def get(self):
        try:
            ingredientArray = getIngredients()
            ingredientList = { 'ingredientArray': ingredientArray }
        except:
            print("Count not retrieve ingredient array")
            return {'ingredientArray': []}

        return ingredientList