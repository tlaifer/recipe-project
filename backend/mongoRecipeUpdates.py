from mongoconnection import mongo_setup
import pymongo

recipeDb = mongo_setup()

def indexIngredients():

    # Index ingredients in ascending order
    recipeDb.create_index( [ ('ingredients', 1) ] )
    print("Ingredients indexed!")

    return

def indexRecipeId():

    # Index recipe IDs in ascending order
    recipeDb.create_index( [ ('recipeId', 1) ] )
    print("Recipe IDs indexed!")

    return

def addRatings():

    #for recipe in recipeDb.find():
    #    recipe.update( { '$set': { '$averageRating': 0 } } )

    recipeDb.update_many({'recipeId': {'$gt': 0}}, {'$set': { 'averageRating': 0 }} )
    print("Added average rating value to recipes!")

    return

def addRatingsTest():

        #recipeDb.update_one({'recipeId': 139209}, {'$set': { 'averageRating': 0 }} )
        #recipeDb.update_many({'recipeId': {'$eq': 338892}}, {'$set': { 'averageRating': 0 }} )
        for recipe in recipeDb.find({'recipeId': 79246}):
            print(recipe)

        return

def checkRecipeIndices():
    print(recipeDb.index_information())

if __name__ == "__main__":
    checkRecipeIndices()

    #indexIngredients()
    #indexRecipeId()
    #addRatingsTest()
    #addRatings()