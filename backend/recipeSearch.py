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
    queryString = """SELECT vetoIngredient FROM vetoedIngredients WHERE userId = {0}""".format(userId)

    try:
        pgCur.execute(queryString)
    except:
        print("Can't retrieve vetoed ingredients.")
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
    queryString = """SELECT technique FROM userTechniques WHERE userId = {0} AND isVeto = {1}""".format(userId, str(vetoed).upper())

    try:
        pgCur.execute(queryString)
    except:
        print("Can't retrieve techniques.")
        return techniques

    rows = pgCur.fetchall()

    if (len(rows) > 0):
        for row in rows:
            techniques.append(row[0])

    return techniques

""" Description: Evaluates whether a recipe contains a vetoed ingredient or technique.
    Returns: A boolean indicating whether or not the recipe contains a vetoed ingredient or technique.
"""
def isEntityVetoed(user, entityArray, vetoedArray):

    if (len(entityArray) <= 0): # nothing is vetoed
        return False

    vetoed = False
    vetoedArray = None

    for entity in entityArray:
        if (entity in vetoedArray):
            vetoed = True
            break

    return vetoed

""" Description: Evaluates whether a recipe should be discarded from the user's recipe search. A recipe
        will be discarded from the search results if it contains at least one vetoed ingredient or technique.
    Returns: A boolean indicating whether or not the recipe should be returned in the search results.
"""
def isRecipeVetoed(userId, recipe, vetoedIngredients, vetoedTechniques):

    recipeIngredients = recipe['ingredients']
    recipeTechniques = recipe['techniques']

    if (len(vetoedIngredients) > 0): # if user has vetoed an ingredient
        if (isEntityVetoed(userId, recipeIngredients, vetoedIngredients) == True):
            return True
    elif (len(vetoedTechniques) > 0): # if user has vetoed a technique
        if (isEntityVetoed(userId, recipeTechniques, vetoedTechniques) == True):
            return True

    return False

""" Description: Function to sort through all recipes and build an array of recipes that meet the user's
        search criteria. The function evaluates all recipes that contain at least one ingredient that the
        user specified, discards recipes that contain a vetoed ingredient or technique, and adds the
        remaining recipes to an array.
    Returns: An array of all recipes that meet the user's search criteria. The recipe objects in the
        resulting array also include a count of specified ingredients, extra ingredients, and preferred
        techniques per recipe.
"""
def buildRecipeArray(userId, ingredientInput):

    recipeDb = mongo_setup()
    recipeArray = []
    recipeCount = 0

    vetoedIngredients = getVetoedIngredients(userId)
    vetoedTechniques = getTechniques(userId, True)
    familiarTechniques = getTechniques(userId, False)

    #userHasVeto = (len(vetoedIngredients) >= 0) or (len(vetoedTechniques) >= 0)

    #for recipe in recipeDb.find({'ingredients': {'$in': ingredientInput}}):
    for recipe in recipeDb.aggregate([ 
        {'$match': {
            '$and': [
                {'ingredients': {'$in': ingredientInput}},
                {'ingredients': {'$nin': vetoedIngredients}},
                {'techniques': {'$nin': vetoedTechniques}}
            ]
        }}
    ]):

        if (recipeCount > 500):
            break

        # Initialize variables
        recipeIngredients = recipe['ingredients']
        recipeTechniques = recipe['techniques']
        ingredientCount = 0
        extraCount = 0
        techniqueCount = 0

        # 4/12 UPDATE: Liz commented out this section because the mongo query excludes vetoed
        #     ingredients and techniques.
        # If there is at least one veto preference, check if we should veto this recipe
        #if (userHasVeto == True):
        #    if (isRecipeVetoed(userId, recipe, vetoedIngredients, vetoedTechniques) == True):
        #        break # recipe is vetoed

        if (len(recipeIngredients) <= 0):
            break # recipe has no ingredients. should not happen, but checking just in case

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
        recipeObject['rating'] = 0 #TODO calculate this
        recipeObject['cookTime'] = recipe['minutes']
        recipeObject['ingredientCount'] = ingredientCount
        recipeObject['extraCount'] = extraCount
        recipeObject['techniqueCount'] = techniqueCount

        recipeArray.append(recipeObject)
        recipeCount += 1

    return recipeArray





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
    recipeArray = buildRecipeArray(1,["basmati rice"])
    return

if __name__ == '__main__':
    main()


class SearchAPI(Resource):
    def post(self):
        parser.add_argument('userId', type=str)
        parser.add_argument('ingredientInput', type=str, action="append")
        args = parser.parse_args()

        try:
            recipeArray = buildRecipeArray(args['userId'], args['ingredientInput'])
            recipeResults = { 'recipeArray': recipeArray }
        except:
            print("Count not retrieve recipe array")
            return {'recipeArray': []}

        return recipeResults #results