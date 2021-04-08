from flask_restful import Api, Resource, reqparse
from .pgconnection import pg_conn


parser = reqparse.RequestParser()

def upsertRating(inputTuple):

    upsert_sql = '''
    INSERT INTO ratings (userId,recipeId, rating, favorite)
        VALUES (%s, %s, NULLIF(%s, 0), NULLIF(%s, 'f'))
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
        cur.close()
        success = True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return success

def getRating(inputTuple):
    sql = """SELECT FROM raings WHERE userId = %s, recipeId = %s"""
    userRow = None
    try:
        conn = pg_conn()
        cur = conn.cursor()
        cur.execute(sql, inputTuple)
        userRow = cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            connection.close()
    return userRow
    

class RatingAPI(Resource):

    def post(self, id):
        parser.add_argument('userId', type=str)
        parser.add_argument('recipeId', type=str)
        parser.add_argument('favorite', type=bool)
        parser.add_argument('rating', type=int)
        args = parser.parse_args()

        return upsertRating((args.userId, args.recipeId, args.favorite, args.rating))

    def get(self, id):
        parser.add_argument('userId', type=str)
        parser.add_argument('recipeId', type=str)
        args = parser.parse_args()

        return getRating((args.userId, args.recipeId))


