from .pgconnection import pg_setup
from flask import jsonify
from flask_restful import fields, marshal_with, reqparse, Resource

pgCur = pg_setup()

def getIngredients(common=True):

    ingredients = []
    if common == False:
        queryString = """SELECT DISTINCT ingredientId, ingredientName FROM ingredients ORDER BY ingredientName"""
    else:
        queryString = """SELECT DISTINCT ingredientId, ingredientName FROM ingredients WHERE common = 't' ORDER BY ingredientName"""

    try:
        pgCur.execute(queryString)
    except:
        print("Can't retrieve ingredients.")
        return ingredients

    rows = pgCur.fetchall()
    if (len(rows) > 0):
        for row in rows:
            ingredients.append({ 'id': row[0], 'name': row[1], 'value': False })

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