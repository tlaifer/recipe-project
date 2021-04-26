from .pgconnection import pg_setup, pg_conn
from flask import jsonify
from flask_restful import fields, marshal_with, reqparse, Resource
import json

parser = reqparse.RequestParser()

pgCur = pg_setup()

def getTechniques(user=False):

    techniques = []
    if (user):
        queryString = """SELECT techniquename, techniqueid, isveto 
                        FROM techniques 
                        LEFT JOIN 
                        ( 
                            SELECT userid, technique, isveto  
                            FROM usertechniques 
                            WHERE userid = %s
                        ) AS ut 
                        ON techniqueid = ut.technique;"""
    else:
        queryString = """SELECT DISTINCT techniquename, techniqueid FROM techniques ORDER BY techniquename"""

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
                'id': row[1],
                'value': row[2] if user else False
            })

    return techniques

def  write_techniques(user, techniques):
    sql1 = """DELETE FROM usertechniques WHERE userid=%s"""
    sql2 = """INSERT INTO usertechniques (userid, technique, isveto) VALUES(%s, %s, %s)"""

    try:
        conn = pg_conn()
        cur = conn.cursor()
        success = True

        cur.execute(sql1, (user,))
        print(f"sql1 {sql1}")
        print(f"{techniques}")
        for technique in techniques:
            ## only write techniques marked as `true` or `false`
            if (technique['value'] != None):
                cur.execute(sql2, (user, technique['id'], technique['value'],))
        
        conn.commit()
    except:
        print("error writing technqiues")

def format_return(arr):
    return jsonify({ 'techniqueArray': arr })

class TechniquesAPI(Resource):
    def put(self):
        parser.add_argument('user', type=int)
        parser.add_argument('techniques', type=dict, action='append')
        args = parser.parse_args()
        return write_techniques(args.user, args.techniques)

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
