from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment

import backend.pgconnection as pgconnection
import backend.mongoconnection as mongoconnection
import backend.recipeSearch as recipeSearch
import backend.ingredients as ingredients
import backend.user as user
import backend.rating as rating

app = Flask(__name__)
CORS(app) #comment this on deployment
api = Api(app)
parser = reqparse.RequestParser()

sample_mongodb_doc = mongoconnection.return_one()
sample_pg = pgconnection.return_pg()

class Hello(Resource):
    def get(self):
        hello = 'welcome to our application'
        return { 'message': hello, 
        'mongoDbRecord' : str(sample_mongodb_doc),
        'pgRecord' : str(sample_pg) }

"""
LJ: Tali and Dominic you can ignore this.
This is my testing function for making sure my API syntax works.
Feel free to use it in Postman yourselves or manipulate the code if needed.
"""
class OneRecipeTest(Resource):
    def post(self):
        parser.add_argument('userId', type=str)
        parser.add_argument('ingredientInput', type=str, action="append")
        args = parser.parse_args()
        
        try:
            recipeArray = recipeSearch.testOneRecipe(args['userId'], args['ingredientInput'])
            recipeResults = { 'recipeArray': recipeArray }
        except:
            print("Count not retrieve recipe array")
            return {'recipeArray': []}

        return recipeResults

class SearchAPI(Resource):
    def post(self):
        parser.add_argument('userId', type=str)
        parser.add_argument('ingredientInput', type=str, action="append")
        args = parser.parse_args()

        try:
            recipeArray = recipeSearch.buildRecipeArray(args['userId'], args['ingredientInput'])
            recipeResults = { 'recipeArray': recipeArray }
        except:
            print("Count not retrieve recipe array")
            return {'recipeArray': []}

        #results = Flask.make_response(jsonify(recipeResults), 200) # LJ: will handle this later when adding a header
        #results.headers['Total-Results'] = len(recipeArray)

        return recipeResults #results

class RecipeAPI(Resource):
    def get(self, id):
        return { f'message': f'retrieve recipe with id {id}' }

class IngredientsAPI(Resource):
    def get(self):
        try:
            ingredientArray = ingredients.getIngredients()
            ingredientList = { 'ingredientArray': ingredientArray }
        except:
            print("Count not retrieve ingredient array")
            return {'ingredientArray': []}

        return ingredientList

# Test APIs
api.add_resource(Hello, '/')
api.add_resource(OneRecipeTest, '/api/oneRecipe/', endpoint='oneRecipe')

# Real APIs
api.add_resource(SearchAPI, '/api/search/', endpoint='search')
api.add_resource(IngredientsAPI, '/api/ingredients/', endpoint='ingredients')
api.add_resource(RecipeAPI, '/api/recipe/<int:id>', endpoint='recipe')
api.add_resource(user.UserAPI, '/api/user/', '/api/user/<int:id>', endpoint='user')
api.add_resource(rating.RatingAPI, '/api/rating/', endpoint='rating')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)