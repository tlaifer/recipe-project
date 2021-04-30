import pgconnection
import psycopg2

def createIngredientStoredFunction():
    conn = pgconnection.pg_conn()

    funct = """
    CREATE OR REPLACE FUNCTION getVetoedIngredients(id INT)
    RETURNS TABLE(ingredient INT) AS $$
    BEGIN
        RETURN QUERY(SELECT vetoIngredient FROM vetoedIngredients WHERE userId = id);
    END;
    $$ LANGUAGE PLPGSQL;
    """

    try:
        cur = conn.cursor() # Connect to the PostgreSQL server
        cur.execute(funct) # Add stored procedure
        cur.close() # Close communication with the PostgreSQL database server
        conn.commit() # Commit the changes

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

    return

def createTechniqueStoredFunction():
    conn = pgconnection.pg_conn()

    funct = """
    CREATE OR REPLACE FUNCTION getTechniques(id INT, vetoBool BOOL)
    RETURNS TABLE(techniques INT) AS $$
    BEGIN
        RETURN QUERY(SELECT technique FROM userTechniques WHERE userId = id AND isVeto = vetoBool);
    END;
    $$ LANGUAGE PLPGSQL;
    """

    try:
        cur = conn.cursor() # Connect to the PostgreSQL server
        cur.execute(funct) # Add stored procedure
        cur.close() # Close communication with the PostgreSQL database server
        conn.commit() # Commit the changes

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

    return

if __name__ == "__main__":
    #createIngredientStoredFunction()
    #createTechniqueStoredFunction()