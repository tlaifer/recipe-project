from flask_restful import Api, Resource, reqparse
from .mongoconnection import mongo_setup
from .pgconnection import pg_conn
from .rating import upsertRating, getRating
from .recipeSearch import getTechniques
import psycopg2
import pymongo

parser = reqparse.RequestParser()

def getFavoriteIds(inputTuple):
    sql = """SELECT recipeId FROM ratings WHERE ratings.userId = %s AND ratings.favorite = 't'"""

    userRow = None
    try:
        conn = pg_conn()
        cur = conn.cursor()
        cur.execute(sql, inputTuple)
        userRow = cur.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        if conn:
            cur.close()
            conn.close()

    return userRow  

def getFavoriteRecipes(userId, favoriteIds):

    recipeDb = mongo_setup()
    recipeArray = []
    recipeCount = 0
    familiarTechniques = getTechniques(userId, False)


    for recipe in recipeDb.aggregate([ 
        {'$match': {'recipeId': {'$in': favoriteIds}}}
    ]):

        if (recipeCount > len(favoriteIds)):
            break

        # Initialize variables
        recipeTechniques = recipe['techniques']
        techniqueCount = 0

        if (len(recipeTechniques) > 0):
            for technique in recipeTechniques:
                if (technique in familiarTechniques):
                    techniqueCount += 1

        recipeObject = {}

        recipeObject['id'] = recipe['recipeId'] # format string so that JSON is properly formatted
        recipeObject['name'] = recipe['recipeName']
        recipeObject['ingredients'] = recipe['ingredients']
        recipeObject['techniques'] = recipeTechniques
        recipeObject['averageRating'] = recipe['averageRating']
        recipeObject['cookTime'] = recipe['minutes']
        recipeObject['techniqueCount'] = techniqueCount

        recipeArray.append(recipeObject)
        recipeCount += 1

    return recipeArray 

def deleteFavorite(inputTuple):

    upsert_sql = '''
    INSERT INTO ratings (userId,recipeId, rating, favorite)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (userId, recipeId)
        DO UPDATE SET
            (rating, favorite)
            = (ratings.rating, EXCLUDED.favorite) ;
    '''

    # input tuple: (userId,recipeId,rating,favorite))
    success = False

    try:
        conn = pg_conn()
        cur = conn.cursor()
        cur.execute(upsert_sql, inputTuple)
        conn.commit()
        success = True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            cur.close()
            conn.close()
    return success    

class FavoriteAPI(Resource):

    def get(self):
        parser.add_argument('userId', type=int)
        args = parser.parse_args()
        userId = args['userId'] if args['userId'] is not None else 1

        print("Getting favorites for user: ")
        print(userId)
        #turn list of tuples into list of ints
        favoriteIdsArray = list(sum(getFavoriteIds((userId,)), ()))
        print("favoriteIds are: ")
        print(favoriteIdsArray)

        favoriteRecipeArray = getFavoriteRecipes(userId, favoriteIdsArray)
        return { 'recipeArray': favoriteRecipeArray }



    def delete(self):
        parser.add_argument('userId', type=int)
        parser.add_argument('recipeId', type=int)
        args = parser.parse_args()
        userId = args['userId'] if args['userId'] is not None else 1

        return deleteFavorite((userId, args['recipeId'], 5, False)) 