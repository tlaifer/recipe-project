from .pgconnection import pg_setup
from flask import jsonify
from flask_restful import Api, Resource, reqparse
from .pgconnection import pg_conn
import psycopg2
import itertools

parser = reqparse.RequestParser()

def insertVetoIngredients(inputTuple):

    insert_sql = '''
    INSERT INTO vetoedIngredients (userId,vetoIngredient)
        VALUES %s
    '''
    success = False

    try:
        conn = pg_conn()
        cur = conn.cursor()
        cur.execute(insert_sql, inputTuple)
        conn.commit()
        success = True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            cur.close()
            conn.close()
    return success

def deleteUserVetoIngredients(inputTuple):
    sql = """DELETE FROM vetoedIngredients WHERE userId = %s"""
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
    
def getUserVetoIngredients(inputTuple):
    sql = """SELECT * FROM vetoedIngredients WHERE userId = %s"""

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


class VetoIngredientsAPI(Resource):

    def post(self):
        parser.add_argument('userId', type=int)
        parser.add_argument('vetoIngredients', type=list)
        args = parser.parse_args()
        userId = args["userId"]
        print(userId)
        print(args["vetoIngredients"])
        tuples = itertools.zip_longest(list(userId),args["vetoIngredients"], fillvalue= userId)

        # Delete all existing entries and then reinsert
        # Could optimize with union set
        deleteUserVetoIngredients((userId,))
        return insertVetoIngredients(tuples)

    def delete(self):
        parser.add_argument('userId', type=int)
        args = parser.parse_args()

        return deleteUserVetoIngredients((args['userId'],))

    def get(self):
        parser.add_argument('userId', type=int)
        args = parser.parse_args()

        return getUserVetoIngredients((args['userId'],))




            