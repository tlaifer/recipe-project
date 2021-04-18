from .pgconnection import pg_setup
from flask import jsonify
from flask_restful import fields, marshal_with, reqparse, Resource
import json

parser = reqparse.RequestParser()

pgCur = pg_setup()

def getTechniques(user=False):

    techniques = []
    if (user):
        queryString = """SELECT techniquename, isveto 
                        FROM techniques 
                        LEFT JOIN 
                        ( 
                            SELECT userid, technique, isveto  
                            FROM usertechniques 
                            WHERE userid = %s
                        ) AS ut 
                        ON techniqueid = ut.technique;"""
    else:
        queryString = """SELECT DISTINCT techniquename FROM techniques ORDER BY techniquename"""

    try:
        print(user)
        print(queryString)
        pgCur.execute(queryString, (user,))
    except:
        print("Can't retrieve techniques.")
        return techniques

    rows = pgCur.fetchall()
    if (len(rows) > 0):
        for row in rows:
            techniques.append({
                'name': row[0],
                'value': row[1] or False if user else False
            })

    return techniques

def format_return(arr):
    return jsonify({ 'techniqueArray': arr })

class TechniquesAPI(Resource):
    def post(self): 
        parser.add_argument('user', type=int)
        args = parser.parse_args()
        return format_return(getTechniques(args.user))

    def get(self):
        try:
            return format_return(getTechniques())
        except:
            print("Count not retrieve techniques array")
            return format_return([])
