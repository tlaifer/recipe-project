from flask import jsonify
from flask_restful import fields, marshal_with, reqparse, Resource

parser = reqparse.RequestParser()

def sortRecipes(recipeArray, sortVariable):

    sortedArray = []

    if (sortVariable in ['ingredientCount', 'techniqueCount']):
        sortDescending = True
    elif (sortVariable == 'extraCount'):
        sortDescending = False
    else:
        return [] # Incorrect sort variable

    sortedArray = sorted(recipeArray, key=lambda recipe: recipe[sortVariable], reverse=sortDescending)

    return sortedArray

class RecipeSortAPI(Resource):

    def post(self):

        parser.add_argument('recipeArray', action='append', type=dict)
        parser.add_argument('sortVariable', type=str)
        args = parser.parse_args()
        sortedArray = []

        try:
            sortedArray = sortRecipes(args['recipeArray'], args['sortVariable'])
            sortedResults = { 'sortedArray': sortedArray }
        except:
            print("Count not retrieve sorted array")
            sortedResults = { 'sortedArray': [] }

        return sortedResults