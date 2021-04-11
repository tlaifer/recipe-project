from .pgconnection import pg_setup
pgCur = pg_setup()

def getIngredients():

    ingredients = []
    queryString = """SELECT DISTINCT ingredientName FROM ingredients ORDER BY ingredientName"""

    try:
        pgCur.execute(queryString)
    except:
        print("Can't retrieve ingredients.")
        return ingredients

    rows = pgCur.fetchall()
    if (len(rows) > 0):
        for row in rows:
            ingredients.append({ 'name': row[0], 'value': False })

    return ingredients