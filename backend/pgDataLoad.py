import psycopg2
import pgconnection
import pandas as pd
import numpy as np
import os
from mongoRecipeLoad import DATA_DIRECTORY
from mongoRecipeLoad import TECHNIQUES_LIST



def create_tables(conn):
    """ source: https://www.postgresqltutorial.com/postgresql-python/create-tables/
    create tables in the PostgreSQL database
    """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            name varchar NOT NULL
            )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS vetoedIngredients (
            userId INT,
            vetoIngredient INT,
            PRIMARY KEY (userId,vetoIngredient)
            )
        """,
        """
        CREATE TABLE IF NOT EXISTS ingredients(
            ingredientId INT PRIMARY KEY, 
            ingredientName varchar(255) NOT NULL,
            common BOOL
            )
        """, 
        """
        CREATE TABLE IF NOT EXISTS techniques(
            techniqueId INT PRIMARY KEY, 
            techniqueName varchar(255) NOT NULL
            )
        """, 
        """ 
        CREATE TABLE IF NOT EXISTS usertechniques (
                userid INT REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
                technique INT REFERENCES techniques(techniqueid) ON UPDATE CASCADE,
                isVeto BOOL,
                CONSTRAINT userTechniques_pkey PRIMARY KEY (userid, technique)
                )
        """,
        """
        CREATE TABLE IF NOT EXISTS ratings(
            userId INT, 
            recipeId INT,
            rating INT DEFAULT 0,
            favorite BOOL DEFAULT 'f',
            CONSTRAINT pk_rating PRIMARY KEY (userId,recipeId)
            )
        """)

    try:
        # # connect to the PostgreSQL server
        cur = conn.cursor()
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

def create_indices(conn):
    command = (
        """
        CREATE INDEX idx_recipeId ON ratings(recipeId);
        """)

    try:
        # # connect to the PostgreSQL server
        cur = conn.cursor()
        # create index one by one
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

def printAllTables(cursor):
    cursor.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
    for table in cursor.fetchall():
        print(table)

def dropTable(table):
    conn = pgconnection.pg_conn()
    conn.cursor().execute("DROP TABLE " + table)
    conn.commit()

    print("Dropped " + table + " table")


def copy_from_file(conn, df, table):
    """
    function take from following source: 
    https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/
    Here we are going save the dataframe on disk as 
    a csv file, load the csv file  
    and use copy_from() to copy it to the table
    """
    # Save the dataframe to disk
    df_path = DATA_DIRECTORY + table + "_dataframe.csv"
    df.to_csv(df_path, index = False, header=False)
    f = open(df_path, 'r')
    cursor = conn.cursor()
    try:
        cursor.copy_from(f, table, sep=",")
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("copy_from_file() done")
    cursor.close()


def loadRatingsDf():
    interaction_df = pd.read_csv(DATA_DIRECTORY+"RAW_interactions.csv")
    interaction_df["favorite"] = interaction_df['user_id'].apply(lambda x: False)
    rating_df = interaction_df[["user_id","recipe_id", "rating", "favorite"]]
    rating_df = rating_df.rename(columns = {"user_id" : "userId", "recipe_id" : "recpieId"})
    return rating_df

def loadTechniquesDf():
    t_df = pd.DataFrame(TECHNIQUES_LIST).rename(columns={0 : "techniqueName"})
    t_df["techniqueId"] = t_df.index
    return t_df[["techniqueId", "techniqueName"]]

def loadIngredientsDf():
    i_df = pd.read_pickle(DATA_DIRECTORY+"ingr_map.pkl")
    i_df = i_df[["id", "replaced"]].rename(columns = {"id" : "ingredientsId", "replaced" : "ingredientName"})
    i_df["ingredientName"] = i_df["ingredientName"].apply(removeComma)
    return i_df.drop_duplicates()

def removeComma(s):
    return s.replace(',', '')


def doDataLoad():

    print("Starting postgres dataload...")

    dropTable("ratings")

    create_tables(pgconnection.pg_conn())

    print("Created all tables, printing all tables in pg...")

    printAllTables(pgconnection.pg_conn().cursor())

    print("loading ratings...")
    copy_from_file(pgconnection.pg_conn(), loadRatingsDf(), "ratings")
    # print("loading techniques...")
    # copy_from_file(pgconnection.pg_conn(), loadTechniquesDf(), "techniques")
    # print("loading ingredients...")
    # copy_from_file(pgconnection.pg_conn(), loadIngredientsDf(), "ingredients")

    print("inserted data to tables, now indexing...")

    create_indices(pgconnection.pg_conn())

    print("finished indexing")


if __name__ == "__main__":
    doDataLoad()
