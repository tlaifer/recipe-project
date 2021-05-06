from .mongoconnection import mongo_setup
from .pgconnection import pg_setup
from flask_restful import Api, Resource, reqparse
import psycopg2
import pymongo

pgCur = pg_setup()
parser = reqparse.RequestParser()

""" Description: Retrieves a list of the user's vetoed ingredients, saved in their user perferences.
    Returns: An array of ingrediients the user has vetoed.
"""
def getVetoedIngredients(userId):

    vetoedIngredients = []
    storedFunctionQuery = """SELECT * FROM getVetoedIngredients({0})""".format(userId)

    try:
        pgCur.execute(storedFunctionQuery)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return vetoedIngredients

    rows = pgCur.fetchall()

    if (len(rows) > 0):
        for row in rows:
            vetoedIngredients.append(row[0])

    return vetoedIngredients

""" Description: Retrieves a list of techniques related to the person using the recipe finder app.
    Parameters: A boolean saying whether or not the function should retrieve vetoed techniques. If the parameter
        is true, the function retrieves vetoed techniques. If it is false, the function retrieves preferred
        techniques.
    Returns: An array of techniques that meet the criteria of the parameter (vetoed vs preferred).
"""
def getTechniques(userId,vetoed):

    techniques = []
    storedFunctionQuery = """SELECT * FROM getTechniques({0}, {1})""".format(userId,str(vetoed).upper())

    try:
        pgCur.execute(storedFunctionQuery)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return techniques

    rows = pgCur.fetchall()

    if (len(rows) > 0):
        for row in rows:
            techniques.append(row[0])

    return techniques

""" Description: Function to sort through all recipes and build an array of recipes that meet the user's
        search criteria. The function evaluates all recipes that contain at least one ingredient that the
        user specified, discards recipes that contain a vetoed ingredient or technique, and adds the
        remaining recipes to an array.
    Returns: An array of all recipes that meet the user's search criteria. The recipe objects in the
        resulting array also include a count of specified ingredients, extra ingredients, and preferred
        techniques per recipe.
"""
def returnRecipes(userId, ingredientInput):

    recipeDb = mongo_setup()
    recipeArray = []
    output = {}
    recipeCount = 0

    vetoedIngredients = getVetoedIngredients(userId)
    vetoedTechniques = getTechniques(userId, True)
    familiarTechniques = getTechniques(userId, False)

    for recipe in recipeDb.aggregate([ 
        {'$match': {
            '$and': [
                {'ingredients': {'$in': ingredientInput}},
                {'ingredients': {'$nin': vetoedIngredients}},
                {'techniques': {'$nin': vetoedTechniques}}
            ]
        }}
    ]):

        if (recipeCount > 100):
            break

        # Initialize variables
        recipeIngredients = recipe['ingredients']
        recipeTechniques = recipe['techniques']
        ingredientCount = 0
        extraCount = 0
        techniqueCount = 0

        if (len(recipeIngredients) <= 0):
            continue # recipe has no ingredients. should not happen, but checking just in case

        for ingredient in recipeIngredients:
            if (ingredient in ingredientInput):
                ingredientCount += 1
            else:
                extraCount += 1

        if (len(recipeTechniques) > 0):
            for technique in recipeTechniques:
                if (technique in familiarTechniques):
                    techniqueCount += 1

        recipeObject = {}

        recipeObject['id'] = recipe['recipeId'] # format string so that JSON is properly formatted
        recipeObject['name'] = recipe['recipeName']
        recipeObject['ingredients'] = recipeIngredients
        recipeObject['techniques'] = recipeTechniques
        recipeObject['averageRating'] = recipe['averageRating']
        recipeObject['cookTime'] = recipe['minutes']
        recipeObject['ingredientCount'] = ingredientCount
        recipeObject['extraCount'] = extraCount
        recipeObject['techniqueCount'] = techniqueCount

        recipeArray.append(recipeObject)
        recipeCount += 1

    output = { 'recipeArray': recipeArray }

    return output

class SearchAPI(Resource):
    def post(self):
        parser.add_argument('userId', type=str)
        parser.add_argument('ingredientInput', type=str, action="append")
        args = parser.parse_args()

        try:
            recipeResults = returnRecipes(args['userId'], args['ingredientInput'])
        except:
            print("Count not retrieve recipe array")
            return {'recipeArray': []}

        return recipeResults





""" TESTING SECTIONS """

def testOneRecipe(userId, ingredientInput):

    oneRecipe = [ {
        'id': "6057e15ad46859706045d8cc",
        'name': 'Grilled Cheese',
        'ingredients': ['bread', 'cheese', 'butter'],
        'techniques': ['grill'],
        'rating': 4.3,
        'cookTime': 10,
        'ingredientCount': 1,
        'extraCount': 2,
        'techniqueCount': 1
    } ]

    return oneRecipe

def main():
    recipeArray = returnRecipes(1,["basmati rice"])
    return

if __name__ == '__main__':
    main()