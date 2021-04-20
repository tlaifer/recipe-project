from mongoconnection import mongo_setup

recipeDb = mongo_setup()

def indexIngredients():

    # Index ingredients in ascending order
    recipeDb.create_index( [ ('$ingredients', 1) ] )
    print("Ingredients indexed!")

    return

def addRatings():

    for recipe in recipeDb.find():
        recipe.update( { '$set': { '$averageRating': 0 } } )

    print("Added average rating value to recipes!")

    return

if __name__ == "__main__":
    indexIngredients()