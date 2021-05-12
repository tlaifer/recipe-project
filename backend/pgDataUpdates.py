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
    RETURNS TABLE(techniques varchar(255)) AS $$
    BEGIN
        RETURN QUERY(SELECT t.techniqueName 
        FROM userTechniques AS ut
        JOIN techniques AS t ON ut.technique = t.techniqueId
        WHERE ut.userId = id AND ut.isVeto = vetoBool);
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

def execute(sql):
    conn = pgconnection.pg_conn()
    try:
        cur = conn.cursor() # Connect to the PostgreSQL server
        cur.execute(sql) # Execute SQL 
        cur.close() # Close communication with the PostgreSQL database server
        conn.commit() # Commit the changes

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

    return

def deleteVetoIngredientProcedure():
    conn = pgconnection.pg_conn()

    procedure = """
    CREATE OR REPLACE PROCEDURE deleteVetoIngredient(uid INT)
    LANGUAGE PLPGSQL
    AS $$
    BEGIN
      DELETE FROM vetoedIngredients WHERE userId = uid;
    END;$$
    """

    try:
        cur = conn.cursor() # Connect to the PostgreSQL server
        cur.execute(procedure) # Add stored procedure
        cur.close() # Close communication with the PostgreSQL database server
        conn.commit() # Commit the changes

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

    return

def deleteRatingProcedure():
    conn = pgconnection.pg_conn()

    procedure = """
    CREATE OR REPLACE PROCEDURE deleteRating(uid INT, rid INT)
    LANGUAGE PLPGSQL
    AS $$
    BEGIN
      DELETE FROM ratings WHERE ratings.userId = uid AND ratings.recipeId = rid;
      COMMIT;
    END;$$
    """

    try:
        cur = conn.cursor() # Connect to the PostgreSQL server
        cur.execute(procedure) # Add stored procedure
        cur.close() # Close communication with the PostgreSQL database server
        conn.commit() # Commit the changes

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

    return

def common_ingredients():
    sql = """
    CREATE VIEW common_ingredients AS SELECT DISTINCT ingredientId, ingredientName FROM ingredients WHERE common = 't';
    """
    execute(sql)

def user_trigger():
    sql1 = """
    CREATE OR REPLACE FUNCTION deleteuserinfo() RETURNS trigger AS $dt$
    BEGIN
        DELETE FROM usertechniques where userid = OLD.id;
        DELETE FROM vetoedingredients where userid = OLD.id;
        RETURN OLD;
    END;
    $dt$ LANGUAGE plpgsql;
    """
    
    sql2 = """
    CREATE TRIGGER UserDeletion
        BEFORE DELETE ON users
    FOR EACH ROW
        EXECUTE PROCEDURE deleteuserinfo();
    """
    execute(sql1)
    execute(sql2)
    
if __name__ == "__main__":
    #createIngredientStoredFunction()
    createTechniqueStoredFunction()
    #common_ingredients()
    #user_trigger()
    #deleteRatingProcedure()
    #deleteVetoIngredientProcedure()
