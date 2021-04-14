from .pgconnection import pg_setup
from flask import jsonify
from flask_restful import fields, marshal_with, reqparse, Resource

pgCur = pg_setup()

def getTechniques():

    techniques = []
    queryString = """SELECT DISTINCT techniqueName FROM techniques ORDER BY techniqueName"""

    try:
        pgCur.execute(queryString)
    except:
        print("Can't retrieve techniques.")
        return techniques

    rows = pgCur.fetchall()
    if (len(rows) > 0):
        for row in rows:
            techniques.append({ 'name': row[0], 'value': False })

    return techniques

class TechniquesAPI(Resource):
    def get(self):
        try:
            techniqueArray = getTechniques()
            techniqueList = { 'techniqueArray': techniqueArray }
        except:
            print("Count not retrieve techniques array")
            return {'techniqueArray': []}

        return techniqueList