import mongoconnection
import pgconnection
import psycopg2
import pymongo

pg_cur = pgconnection.pg_setup()


#TODO: write header
def get_user_prefs(data, user):
    #TODO: add error handling if data isn't a column name
    query_string = """SELECT {0} FROM users WHERE userId = {1}""".format(data, user)
    pg_cur.execute(query_string)
    
    entity_array = pg_cur.fetchone()
    entity_array = entity_array[0]

    if (entity_array is None):
        entity_array = []

    return entity_array


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


#TODO: make global variables, write header
def is_recipe_vetoed(recipe, vetoed_ingredients, vetoed_techniques):

    recipe_ingredients = recipe['ingredients']
    recipe_techniques = recipe['techniques']

    #TODO: get user 1 out of here
    if (len(vetoed_ingredients) > 0): # if recipe has a vetoed ingredient
        if (is_entity_vetoed(1, recipe_ingredients, vetoed_ingredients) == True):
            return True
    elif (len(vetoed_techniques) > 0): # if recipe has a vetoed technique
        if (is_entity_vetoed(1, recipe_techniques, vetoed_techniques) == True):
            return True

    return False


#TODO: write header
def main():
    recipe_db = mongoconnection.mongo_setup()

    #TODO: get user 1 out of here
    #familiar_techniques = get_user_prefs('familiarTechniques', 1)
    familiar_techniques = [1,2] #TODO: fix familiar technique lookup
    vetoed_ingredients = [] #TODO get_user_prefs('vetoedIngredients', 1)
    vetoed_techniques = get_user_prefs('vetoedTechniques', 1)

    for recipe in recipe_db.find():

        # Initialize variables
        recipe_ingredients = recipe['ingredients']
        recipe_techniques = recipe['techniques']
        ingredient_count = 0
        extra_count = 0
        technique_count = 0

        # If there is at least one veto preference, check if we should veto this recipe
        if ((len(vetoed_ingredients) >= 0) or (len(vetoed_techniques) >= 0)):
            if (is_recipe_vetoed(recipe, vetoed_ingredients, vetoed_techniques) == True):
                break # recipe is vetoed

        for technique in recipe_techniques:
            if (technique in familiar_techniques):
                technique_count += 1

    #TODO: evaluate ingredients passed in from search and increment ingredient and extra counts
    #TODO: build recipe dictionaries here (or make a function to build them)

    return


if __name__ == '__main__':
    main()