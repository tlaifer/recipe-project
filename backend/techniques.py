from .pgconnection import pg_setup
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