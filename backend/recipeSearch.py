from .mongoconnection import mongo_setup
from .pgconnection import pg_setup
import psycopg2
import pymongo

#TODO error handling:
#1. Will ingredient input always be > 0?
#2. Will client prevent user from picking an input ingredient that is also a vetoed ingredient?

pgCur = pg_setup()

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

    vetoedIngredients = getVetoedIngredients(userId)
    vetoedTechniques = getTechniques(userId, True)
    familiarTechniques = getTechniques(userId, False)

    userHasVeto = (len(vetoedIngredients) >= 0) or (len(vetoedTechniques) >= 0)

    for recipe in recipeDb.find({'ingredients': {'$in': ingredientInput}}):

        # Initialize variables
        recipeIngredients = recipe['ingredients']
        recipeTechniques = recipe['techniques']
        ingredientCount = 0
        extraCount = 0
        techniqueCount = 0

        # If there is at least one veto preference, check if we should veto this recipe
        if (userHasVeto == True):
            if (isRecipeVetoed(userId, recipe, vetoedIngredients, vetoedTechniques) == True):
                break # recipe is vetoed

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

        recipeObject['id'] = str(recipe['_id']) # format string so that JSON is properly formatted
        recipeObject['name'] = recipe['recipeName']
        recipeObject['ingredients'] = recipeIngredients
        recipeObject['techniques'] = recipeTechniques
        recipeObject['rating'] = 0 #TODO calculate this
        recipeObject['cookTime'] = recipe['minutes']
        recipeObject['ingredientCount'] = ingredientCount
        recipeObject['extraCount'] = extraCount
        recipeObject['techniqueCount'] = techniqueCount

        recipeArray.append(recipeObject)

    return recipeArray





""" TESTING SECTIONS """

def testOneRecipe(userId, ingredientInput):

    oneRecipe = [ {
        'id': 1,
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