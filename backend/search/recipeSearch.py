import backend.dataload.mongoconnection as mongoconnection
import backend.dataload.pgconnection as pgconnection
import psycopg2
import pymongo

#TODO error handling:
#1. Will ingredient input always be > 0?
#2. Will client prevent user from picking an input ingredient that is also a vetoed ingredient?

pg_cur = pgconnection.pg_setup()
user_id = 1 #TODO: get this from client
ingredient_input = [
        "basmati rice",
        "water",
        "salt",
        "cinnamon stick",
        "green cardamom pods"
      ]
 #TODO: get this from client

""" Description: Retrieves a list of the user's vetoed ingredients, saved in their user perferences.
    Returns: An array of ingrediients the user has vetoed.
"""
def get_vetoed_ingredients():

    vetoed_ingredients = []
    query_string = """SELECT vetoIngredient FROM vetoedIngredients WHERE userId = {0}""".format(user_id)

    try:
        pg_cur.execute(query_string)
    except:
        print("Can't retrieve vetoed ingredients.")
        return vetoed_ingredients

    rows = pg_cur.fetchall()

    if (len(rows) > 0):
        for row in rows:
            vetoed_ingredients.append(row[0])

    return vetoed_ingredients

""" Description: Retrieves a list of techniques related to the person using the recipe finder app.
    Parameters: A boolean saying whether or not the function should retrieve vetoed techniques. If the parameter
        is true, the function retrieves vetoed techniques. If it is false, the function retrieves preferred
        techniques.
    Returns: An array of techniques that meet the criteria of the parameter (vetoed vs preferred).
"""
def get_techniques(vetoed):

    techniques = []
    query_string = """SELECT technique FROM userTechniques WHERE userId = {0} AND isVeto = {1}""".format(user_id, str(vetoed).upper())

    try:
        pg_cur.execute(query_string)
    except:
        print("Can't retrieve techniques.")
        return techniques

    rows = pg_cur.fetchall()

    if (len(rows) > 0):
        for row in rows:
            techniques.append(row[0])

    return techniques

""" Description: Evaluates whether a recipe contains a vetoed ingredient or technique.
    Returns: A boolean indicating whether or not the recipe contains a vetoed ingredient or technique.
"""
def is_entity_vetoed(user, entity_array, vetoed_array):

    if (len(entity_array) <= 0): # nothing is vetoed
        return False

    vetoed = False
    vetoed_array = None

    for entity in entity_array:
        if (entity in vetoed_array):
            vetoed = True
            break

    return vetoed

""" Description: Evaluates whether a recipe should be discarded from the user's recipe search. A recipe
        will be discarded from the search results if it contains at least one vetoed ingredient or technique.
    Returns: A boolean indicating whether or not the recipe should be returned in the search results.
"""
def is_recipe_vetoed(recipe, vetoed_ingredients, vetoed_techniques):

    recipe_ingredients = recipe['ingredients']
    recipe_techniques = recipe['techniques']

    if (len(vetoed_ingredients) > 0): # if user has vetoed an ingredient
        if (is_entity_vetoed(user_id, recipe_ingredients, vetoed_ingredients) == True):
            return True
    elif (len(vetoed_techniques) > 0): # if user has vetoed a technique
        if (is_entity_vetoed(user_id, recipe_techniques, vetoed_techniques) == True):
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
def build_recipe_array():

    recipe_db = mongoconnection.mongo_setup()
    recipe_array = []

    vetoed_ingredients = get_vetoed_ingredients()
    vetoed_techniques = get_techniques(True)
    familiar_techniques = get_techniques(False)

    user_has_veto = (len(vetoed_ingredients) >= 0) or (len(vetoed_techniques) >= 0)

    for recipe in recipe_db.find({'ingredients': {'$in': ingredient_input}}):

        # Initialize variables
        recipe_ingredients = recipe['ingredients']
        recipe_techniques = recipe['techniques']
        ingredient_count = 0
        extra_count = 0
        technique_count = 0

        # If there is at least one veto preference, check if we should veto this recipe
        if (user_has_veto == True):
            if (is_recipe_vetoed(recipe, vetoed_ingredients, vetoed_techniques) == True):
                break # recipe is vetoed

        if (len(recipe_ingredients) <= 0):
            break # recipe has no ingredients. should not happen, but checking just in case

        for ingredient in recipe_ingredients:
            if (ingredient in ingredient_input):
                ingredient_count += 1
            else:
                extra_count += 1

        if (len(recipe_techniques) > 0):
            for technique in recipe_techniques:
                if (technique in familiar_techniques):
                    technique_count += 1

        recipe['_id'] = str(recipe['_id']) # format string so that JSON is properly formatted
        recipe['ingredient_count'] = ingredient_count
        recipe['extra_count'] = extra_count
        recipe['technique_count'] = technique_count

        recipe_array.append(recipe)

    return recipe_array

#TODO: remove this section, it is just here for testing/debugging
def main():
    recipe_array = build_recipe_array()
    return

if __name__ == '__main__':
    main()