from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment

import backend.pgconnection as pgconnection
import backend.mongoconnection as mongoconnection
import backend.ingredients as ingredients
import backend.rating as rating
import backend.recommendedRecipes as recommendedRecipes
import backend.recipeSearch as recipeSearch
import backend.recipeSort as recipeSort
import backend.singleRecipe as singleRecipe
import backend.techniques as techniques
import backend.user as user
import backend.vetoIngredients as vetoIngredients
import backend.favorite as favorite

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

# Test APIs
api.add_resource(Hello, '/')
api.add_resource(OneRecipeTest, '/api/oneRecipe/', endpoint='oneRecipe')

# Searching and Recommendations
api.add_resource(recipeSearch.SearchAPI, '/api/search/', endpoint='search')
api.add_resource(recipeSort.RecipeSortAPI, '/api/recipeSort/', endpoint='recipeSort')
api.add_resource(recommendedRecipes.RecommendationAPI, '/api/recommendations/', endpoint='recommendations')

# Static Info
api.add_resource(ingredients.IngredientsAPI, '/api/ingredients/', endpoint='ingredients')
api.add_resource(techniques.TechniquesAPI, '/api/techniques/', endpoint='techniques')
api.add_resource(singleRecipe.RecipeAPI, '/api/recipe/<int:id>', endpoint='recipe')

# User Information
api.add_resource(user.UserAPI, '/api/user/', '/api/user/<int:id>', endpoint='user')
api.add_resource(rating.RatingAPI, '/api/rating/', endpoint='rating')
api.add_resource(user.UsersAPI, '/api/users/', endpoint='users')
api.add_resource(vetoIngredients.VetoIngredientsAPI, '/api/vetoIngredients/', endpoint='vetoIngredients')
api.add_resource(favorite.FavoriteAPI, "/api/favorite/", endpoint='favorite')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)