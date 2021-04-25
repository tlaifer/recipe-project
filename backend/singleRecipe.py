from .mongoconnection import mongo_setup
from flask_restful import Api, Resource, reqparse
import psycopg2

def singleRecipe(recipeId):

    recipeDb = mongo_setup()
    recipeObject = {}

    recipe = recipeDb.find_one({ 'recipeId': recipeId })

    recipeObject['id'] = recipe['recipeId']
    recipeObject['name'] = recipe['recipeName']
    recipeObject['ingredients'] = recipe['ingredients']
    recipeObject['techniques'] = recipe['techniques']
    recipeObject['description'] = recipe['description']
    recipeObject['averageRating'] = recipe['averageRating']
    recipeObject['cookTime'] = recipe['minutes']

    return recipeObject

class RecipeAPI(Resource):

    def get(self, id):
        recipe = singleRecipe(id)
        return recipe


# TESTING SECTIONS
def main():
    singleRecipe(450478)
    return
if __name__ == '__main__':
    main()