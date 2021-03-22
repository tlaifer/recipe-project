import pyconnection
import pandas as pd
import numpy as np
import DATA_DIRECTORY from mongoRecipeLoad
import TECHNIQUES_LIST from mongoRecipeLoad


def create_tables():
    """ source: https://www.postgresqltutorial.com/postgresql-python/create-tables/
    create tables in the PostgreSQL database
    """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users(
            userId INT PRIMARY KEY, 
            username varchar(255) NOT NULL
            )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS vetoedIngredients (
                id INT PRIMARY KEY,
                userId INT,
                vetoIngredient INT
                )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS userTechniques (
                id INT PRIMARY KEY,
                userId INT,
                technique INT
                isVeto BOOL
                )
        """,
        """
        CREATE TABLE IF NOT EXISTS ingredients(
            ingredientId INT PRIMARY KEY, 
            ingredientName varchar(255) NOT NULL
            )
        """, 
        """
        CREATE TABLE IF NOT EXISTS techniques(
            techniqueId INT PRIMARY KEY, 
            techniqueName varchar(255) NOT NULL
            )
        """, 
        """
        CREATE TABLE IF NOT EXISTS ratings(
            userId INT PRIMARY KEY, 
            recipeId INT PRIMARY KEY,
            favorite BOOL DEFAULT 'f'
            rating numeric DEFAULT 0
            )
        """)

        conn = None
    try:
        # # read the connection parameters
        params = config()
        # # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = pgconnection.pg_setup()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def copy_from_file(conn, df, table):
    """
    function take from following source: 
    https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/
    Here we are going save the dataframe on disk as 
    a csv file, load the csv file  
    and use copy_from() to copy it to the table
    """
    # Save the dataframe to disk
    tmp_df = "./tmp_dataframe.csv"
    df.to_csv(tmp_df, index_label='id', header=False)
    f = open(tmp_df, 'r')
    cursor = conn.cursor()
    try:
        cursor.copy_from(f, table, sep=",")
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        os.remove(tmp_df)
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("copy_from_file() done")
    cursor.close()
    os.remove(tmp_df)


def loadRatingDf():
    interation_df = pd.read_csv(DATA_DIRECTORY+"RAW_interactions.csv")
    rating_df = interaction_df["user_id","recipe_id", "rating", "review"]
    return rating_df.rename(columns = {"user_id" : "userId","recipe_id" : "recpieId"})

def loadTechniqueDf():
    t_df = pd.DataFrame(TECHNIQUES_LIST).rename(columns={0 : "techniqueName"})
    t_df["techniqueId"] = t_df.index
    return t_df[["techniqueId", "techniqueName"]]

def loadIngredientsDf():
    i_df = pd.read_pickle(DATA_DIRECTORY+"ingr_map.pkl")
    i_df = i_df[["id", "replaced"]].rename(columns = {"id" : "ingredientsId", "replaced" : "ingredientName"})
    return i_df.drop_duplicates()


