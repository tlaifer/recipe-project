from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment

import backend.pgconnection as pgconnection
import backend.mongoconnection as mongoconnection
import backend.recipeSearch as recipeSearch
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

class SearchAPI(Resource):
    def post(self):
        parser.add_argument('userId', type=str)
        parser.add_argument('ingredientInput', type=[str])
        args = parser.parse_args()

        recipeArray = recipeSearch.buildRecipeArray(args['userId'], args['ingredientInput'])
        recipeResults = { 'recipeArray': recipeArray }
        return recipeResults

class RecipeAPI(Resource):
    def get(self, id):
        return { f'message': f'retrieve recipe with id {id}' }

api.add_resource(Hello, '/')
api.add_resource(SearchAPI, '/api/search/', endpoint='search')
api.add_resource(RecipeAPI, '/api/recipe/<int:id>', endpoint='recipe')
api.add_resource(user.UserAPI, '/api/user/', '/api/user/<int:id>', endpoint='user')
api.add_resource(rating.RatingAPI, '/api/rating/', endpoint='rating')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)