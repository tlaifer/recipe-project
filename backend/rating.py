from flask_restful import Api, Resource, reqparse
from .pgconnection import pg_conn
import psycopg2

parser = reqparse.RequestParser()

def upsertRating(inputTuple):

    upsert_sql = '''
    INSERT INTO ratings (userId,recipeId, rating, favorite)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (userId, recipeId)
        DO UPDATE SET
            (rating, favorite)
            = (EXCLUDED.rating, EXCLUDED.favorite) ;
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

def getRating(inputTuple):
    sql = """SELECT * FROM ratings WHERE ratings.userId = %s AND ratings.recipeId = %s"""

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

def deleteRating(inputTuple):
    sql = """DELETE FROM ratings WHERE ratings.userId = %s AND ratings.recipeId = %s"""
    success = False
    try:
        conn = pg_conn()
        cur = conn.cursor()
        cur.execute(sql, inputTuple)
        conn.commit()
        success = True
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        if conn:
            cur.close()
            conn.close()
    return success

def recalculateAverageRating(recipeId):

    averageRating = 0
    sql = """SELECT AVG(rating) AS 'averageRating' FROM ratings WHERE ratings.recipeId = %s"""

    try:
        conn = pg_conn()
        cur = conn.cursor()
        cur.execute(sql, recipeId)
        avg = cur.fetchone()
        averageRating = avg['averageRating']

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        if conn:
            cur.close()
            conn.close()

    return averageRating
    

class RatingAPI(Resource):

    def post(self):
        parser.add_argument('userId', type=int)
        parser.add_argument('recipeId', type=int)
        parser.add_argument('rating', type=int)
        parser.add_argument('favorite', type=bool)
        args = parser.parse_args()

        #can't rely on default value in pg for some reason
        #also appears that anything that isn't null is true somehow
        #set default user if none passed in since front 
        userId = args['userId'] if args['userId'] is not None else 1
        fav = args['favorite'] if args['favorite'] is not None else False
        rating = args['rating'] if args['rating'] is not None  else 0

        final_args = (userId, args['recipeId'], rating, fav)
        print(final_args)

        #TODO: recalculate/insert new average rating
        
        return upsertRating(final_args)

    def get(self):
        parser.add_argument('userId', type=int)
        parser.add_argument('recipeId', type=int)
        args = parser.parse_args()
        return getRating((args['userId'], args['recipeId']))

    def delete(self):
        parser.add_argument('userId', type=int)
        parser.add_argument('recipeId', type=int)
        args = parser.parse_args()
        return deleteRating((args['userId'], args['recipeId']))