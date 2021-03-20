import mongoconnection
import pgconnection
import psycopg2
import pymongo

#TODO: write header
def get_user_prefs(pg_cur, data, user):
    #TODO: add error handling if data isn't a column name
    query_string = """SELECT {0} FROM users WHERE userId = {1}""".format(data, user)
    pg_cur.execute(query_string)
    
    vetoed_array = pg_cur.fetchone()
    vetoed_array = vetoed_array[0]

    if (vetoed_array is None):
        vetoed_array = []

    return vetoed_array


#TODO: write header
def is_vetoed(pg_cur, user, entity_array, vetoed_array):

    if (len(entity_array) <= 0): # nothing is vetoed
        return False

    vetoed = False
    vetoed_array = None

    for entity in entity_array:
        if (entity in vetoed_array):
            vetoed = True
            break

    return vetoed

#TODO: break into smaller functions
def main():
    recipe_db = mongoconnection.mongo_setup()
    pg_cur = pgconnection.pg_setup()

    #TODO: get user 1 out of here
    #familiar_techniques = get_user_prefs(pg_cur, 'familiarTechniques', 1)
    #familiar_technique_count = len(familiar_techniques)

    vetoed_ingredients = [] #TODO get_user_prefs(pg_cur, 'vetoedIngredients', 1)
    vetoed_ingredient_count = len(vetoed_ingredients)

    vetoed_techniques = get_user_prefs(pg_cur, 'vetoedTechniques', 1)
    vetoed_technique_count = len(vetoed_techniques)

    for recipe in recipe_db.find():
        vetoed = False
        recipe_ingredients = recipe['ingredients']
        recipe_techniques = recipe['techniques']

        #TODO use real user ID
        if (vetoed_ingredient_count > 0):
            vetoed = is_vetoed(pg_cur, 1, recipe_ingredients, vetoed_ingredients)
            if (vetoed == True): # quit if an ingredient is vetoed
                break

        #TODO use real user ID
        if (vetoed_technique_count > 0):
            vetoed = is_vetoed(pg_cur, 1, recipe_techniques, vetoed_ingredients)
            if (vetoed == True): # quit if a technique is vetoed
                break

        for technique in recipe_techniques:
            pass #TODO: count preferred techniques

    #TODO: evaluate ingredients passed in from search and increment ingredient and extra counts
    #TODO: build recipe dictionaries here (or make a function to build them)

    return

if __name__ == '__main__':
    main()