from .mongoconnection import mongo_setup
from .pgconnection import pg_setup
from flask_restful import Api, Resource, reqparse
import psycopg2

pgCur = pg_setup()
parser = reqparse.RequestParser()
recipeDb = mongo_setup()

def findRecommendRecipes(uid):

    recommendedRecipesInit = []
    recommendedRecipes = []

    query = """
    WITH usersFavoriteRecipes AS (
        SELECT recipeId
        FROM ratings
        WHERE userId = {0}
            AND ((favorite = TRUE) OR (rating >= 4))
    ), othersWithSameFavorites AS (
        SELECT userId
        FROM ratings
        WHERE recipeId IN (SELECT * FROM usersFavoriteRecipes)
            AND ((favorite = TRUE) OR (rating >= 4))
    )
    SELECT recipeId
    FROM ratings
    WHERE userId IN (SELECT * FROM othersWithSameFavorites)
        AND recipeId NOT IN (SELECT * FROM usersFavoriteRecipes)
        AND ((favorite = TRUE) OR (rating >= 4))
    GROUP BY recipeId
    ORDER BY COUNT(*) DESC
    LIMIT 10
    """.format(uid)

    try:
        pgCur.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return recommendedRecipes

    rows = pgCur.fetchall()

    if (len(rows) > 0):
        for row in rows:
            recommendedRecipesInit.append(row[0])

    for recipe in recommendedRecipesInit:

        for fullRecipe in recipeDb.find( { 'recipeId': recipe } ): # Should be just one

            if (fullRecipe == None):
                continue # Go to next recipe if ID is invalid for some reason

            recipeObject = {}

            recipeObject['id'] = fullRecipe['recipeId']
            recipeObject['name'] = fullRecipe['recipeName']
            recipeObject['ingredients'] = fullRecipe['ingredients']
            recipeObject['techniques'] = fullRecipe['techniques']
            recipeObject['averageRating'] = fullRecipe['averageRating']
            recipeObject['cookTime'] = fullRecipe['minutes']

            recommendedRecipes.append(recipeObject)

    return recommendedRecipes



class RecommendationAPI(Resource):

    def post(self):
        parser.add_argument('userId', type=int)
        args = parser.parse_args()

        try:
            recommendedRecipeArray = findRecommendRecipes(args['userId'])
            recommendedRecipes = { 'recommendedRecipeArray': recommendedRecipeArray }
        except:
            print("Count not retrieve recommended recipe array")
            return { 'recommendedRecipes': [] }

        return recommendedRecipes