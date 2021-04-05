import psycopg2

def return_pg():
    stringToReturn = None
    try:
        pg_conn = psycopg2.connect(dbname="recipe_dev", user="postgres", password="postgres")
    except:
        print("Unable to connect to the database.")
        return
    
    cur = pg_conn.cursor()
    try:
        cur.execute("""SELECT * from ratings LIMIT 2""")
    except:
        print("Can't SELECT from ratings")
        
    rows = cur.fetchall()
    stringToReturn = "\nPG Rating Rows: \n"
    for row in rows:
        stringToReturn+= "   " + str(row)
    
    return stringToReturn

def pg_setup():

    pg_connection = pg_conn()

    cur = pg_connection.cursor()

    return cur

def pg_conn():
    try:
        pg_conn = psycopg2.connect(dbname="recipe_dev", user="postgres", password="postgres")
    except:
        print("Unable to connect to the database.")
    return pg_conn
