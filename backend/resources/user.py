from flask_restful import fields, marshal_with, reqparse, Resource
from backend.dataload.pgconnection import pg_conn


def sqlHelper(sqlStatement, inputTuple, func):
    toReturn = False
    try:
        conn = pg_conn()
        cur = conn.cursor()
        cur.execute(sql, inputTuple)
        if (func == "create"):
            toReturn = cur.fetchone()[0]
        elif (func == "update" or func == "delete"):
            toReturn = cur.rowcount > 0
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return toReturn


def createUser(userName):
    sql = """INSERT INTO users(userName)
             VALUES(%s) RETURNING userId;"""
    return sqlHelper(sql, (userName,), "create")

def updateUser(userId, userName):
    sql = """ UPDATE users
                SET userName = %s
                WHERE userId = %s"""
    return sqlHelper(sql, (userName, userId), "update")

def deleteUser(userId):
    sql = """DELETE FROM users WHERE userId = %s"""
    
    return sqlHelper(sql, (userId,), "update") 

def getUser(userId):
    sql = """SELECT FROM users WHERE userId = %s"""
    try:
        conn = pg_conn()
        cur = conn.cursor()
        cur.execute(sql, (userId,))
        userRow = cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            connection.close()

def getAllUsers():
    sql = """SELECT * FROM users"""
    try:
        conn = pg_conn()
        cur = conn.cursor()
        cur.execute(sql)
        userRow = cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            connection.close()
    

class UserAPI(Resource):

    def get(self, id):
        return getUser(id)

    def put(self, id):
        # should be name, need to figure out how to pass args
        return createUser(id)

    def delete(self, id):
        return deleteUser(id)