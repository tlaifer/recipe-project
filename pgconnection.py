import psycopg2

def return_pg():
    stringToReturn = None
    try:
        pg_conn = psycopg2.connect(dbname="recipe_dev", user="postgres", password="postgres")
    except:
        print("Unable to connect to the database.")
    
    cur = pg_conn.cursor()
    try:
        cur.execute("""SELECT * from users""")
    except:
        print("Can't SELECT from users")
        
    rows = cur.fetchall()
    stringToReturn = "\nPG User Rows: \n"
    for row in rows:
        stringToReturn+= "   " + str(row)
    
    return stringToReturn

def pg_setup():

    cur = None

    try:
        pg_conn = psycopg2.connect(dbname="recipe_dev", user="postgres", password="postgres")
    except:
        print("Unable to connect to the database.")

    cur = pg_conn.cursor()

    return cur