import mongoconnection
import pgconnection
import psycopg2
import pymongo

#TODO error handling:
#1. Will ingredient input always be > 0?
#2. Will client prevent user from picking an input ingredient that is also a vetoed ingredient?

pg_cur = pgconnection.pg_setup()
user_id = 1 #TODO: get this from client
ingredient_input = [1,2,3] #TODO: get this from client

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

#TODO: write header
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

#TODO: write header
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

#TODO: write header
def main():
    recipe_db = mongoconnection.mongo_setup()

    vetoed_ingredients = get_vetoed_ingredients()
    vetoed_techniques = get_techniques(True)
    familiar_techniques = get_techniques(False)
    
    user_has_veto = (len(vetoed_ingredients) >= 0) or (len(vetoed_techniques) >= 0)

    for recipe in recipe_db.find():

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
    
    #TODO: build recipe dictionaries here (or make a function to build them)

    return


if __name__ == '__main__':
    main()