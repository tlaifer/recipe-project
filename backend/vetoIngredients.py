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
        VALUES (%(userId)s, %(vetoIngredient)s)
    '''
    success = False

    print(insert_sql)
    print(inputTuple)

    try:
        conn = pg_conn()
        cur = conn.cursor()
        cur.executemany(insert_sql, inputTuple)
        conn.commit()
        success = True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            cur.close()
            conn.close()
    return success

def deleteUserVetoIngredients(userId):
    #sql = """DELETE FROM vetoedIngredients WHERE userId = %s"""
    sql_proc = """CALL deleteVetoIngredient({0})""".format(userId)
    success = False
    try:
        conn = pg_conn()
        cur = conn.cursor()
        cur.execute(sql_proc)
        conn.commit()
        success = True
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        if conn:
            cur.close()
            conn.close()
    return success   
    
def getUserVetoIngredients(uid):
    sql = """
          SELECT i.ingredientName
          FROM vetoedIngredients AS vi
          LEFT JOIN ingredients AS i ON vi.vetoIngredient = i.ingredientId
          WHERE userId = {0}
          """

    results = {}
    userRow = []
    vetoedIngredientArray = []

    try:
        conn = pg_conn()
        cur = conn.cursor()
        print(sql.format(uid))
        cur.execute(sql.format(uid))
        userRow = cur.fetchall()

        for vetoedIngredient in userRow:
            vetoedIngredientObject = {}
            vetoedIngredientObject = { 'name':  vetoedIngredient[0]}

            vetoedIngredientArray.append(vetoedIngredientObject)

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        if conn:
            cur.close()
            conn.close()
    
    results = { 'vetoedIngredients': vetoedIngredientArray }

    print(results)

    return results


class VetoIngredientsAPI(Resource):

    def post(self):
        parser.add_argument('userId', type=int)
        parser.add_argument('vetoIngredients', type=dict, action='append')
        args = parser.parse_args()
        userId = args["userId"]
        print("userId: " + str(userId))
        tuples = []
        if (args["vetoIngredients"] != None):
            for i in args["vetoIngredients"]:
                tuples.append({"userId": userId, "vetoIngredient": i["id"]})
        print("Tuples: " + str(tuples))

        # Delete all existing entries and then reinsert
        # Could optimize with union set
        deleteUserVetoIngredients(userId)
        print("Delete successful")
        return insertVetoIngredients(tuples)

    def delete(self):
        parser.add_argument('userId', type=int)
        args = parser.parse_args()

        return deleteUserVetoIngredients(args['userId'])

    def get(self):
        parser.add_argument('userId', type=int, location='args')
        args = parser.parse_args()

        return getUserVetoIngredients(args['userId'])




            