import psycopg2
from flask import jsonify
from flask_restful import fields, marshal_with, reqparse, Resource
from .pgconnection import pg_conn
import json

parser = reqparse.RequestParser()

def sqlHelper(sqlStatement, inputTuple, func):
    toReturn = False
    try:
        conn = pg_conn()
        cur = conn.cursor()
        cur.execute(sqlStatement, inputTuple)
        if (func == "create"):
            toReturn = cur.fetchone()[0]
        elif (func == "update" or func == "delete"):
            toReturn = cur.rowcount > 0
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return toReturn


def createUser(name):
    sql = """INSERT INTO users(name)
             VALUES(%s) RETURNING id;"""
    return  {
        "id": sqlHelper(sql, (name,), "create"),
        "name": name
    }

def updateUser(id, name):
    sql = """ UPDATE users
                SET name = %s
                WHERE id = %s"""
    return sqlHelper(sql, (name, name), "update")

def deleteUser(id):
    sql = """DELETE FROM users WHERE id = %s"""

    return sqlHelper(sql, (id,), "update") 

def getUser(id):
    sql = """SELECT FROM users WHERE id = %s"""
    try:
        conn = pg_conn()
        cur = conn.cursor()
        cur.execute(sql, (id,))
        userRow = cur.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        if conn:
            cur.close()
            conn.close()

def getAllUsers():
    sql = """SELECT * FROM users"""
    userRows = None
    try:
        conn = pg_conn()
        cur = conn.cursor()
        cur.execute(sql)
        userRows = cur.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        if conn:
            cur.close()
            conn.close()
    return userRows

class UsersAPI(Resource):
    def get(self):
        pgUserRows = getAllUsers()
        users = []
        for user in pgUserRows:
            users.append({
                "id": user[0],
                "name": user[1]
            })
        return jsonify(users)

class UserAPI(Resource):
    def get(self, id):
        return getUser(id)

    def put(self):
        parser.add_argument('name', type=str)
        args = parser.parse_args()
        user = createUser(args.name)
        return jsonify(user)

    def delete(self, id):
        return deleteUser(id)