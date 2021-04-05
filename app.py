from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment

import backend.dataload.pgconnection as pgconnection
import backend.dataload.mongoconnection as mongoconnection
import backend.search.recipeSearch
import backend.resources.user as user

app = Flask(__name__)
CORS(app) #comment this on deployment
api = Api(app)

sample_mongodb_doc = mongoconnection.return_one()
sample_pg = pgconnection.return_pg()

class Hello(Resource):
    def get(self):
        hello = 'welcome to our application'
        return { 'message': hello, 
        'mongoDbRecord' : str(sample_mongodb_doc),
        'pgRecord' : str(sample_pg) }

class SearchAPI(Resource):
    def get(self):
        recipeArray = backend.search.recipeSearch.buildRecipeArray()
        recipeResults = { 'recipeArray': recipeArray }
        return recipeResults

class RecipeAPI(Resource):
    def get(self, id):
        return { f'message': f'retrieve recipe with id {id}' }

api.add_resource(Hello, '/')
api.add_resource(SearchAPI, '/api/search/', endpoint='search')
api.add_resource(RecipeAPI, '/api/recipe/<int:id>', endpoint='recipe')
api.add_resource(user.UserAPI, '/api/user/<int:id>', endpoint='user')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)