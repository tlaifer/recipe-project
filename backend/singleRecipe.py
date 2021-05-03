from .mongoconnection import mongo_setup
from flask import jsonify
from flask_restful import Api, Resource, reqparse
import psycopg2

def singleRecipe(recipeId):
    recipeDb = mongo_setup()

    ## return all fields on document obj besides internal _id
    return recipeDb.find_one({ 'recipeId': recipeId }, {"_id": 0})

class RecipeAPI(Resource):

    def get(self, id):
        return jsonify(singleRecipe(id))


# TESTING SECTIONS
def main():
    singleRecipe(450478)
    return
if __name__ == '__main__':
    main()