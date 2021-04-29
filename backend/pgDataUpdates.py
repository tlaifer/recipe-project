import pgconnection
import psycopg2

def createUserStoredProcedure():
    conn = pgconnection.pg_conn()

    procedure = """
    CREATE OR REPLACE PROCEDURE getVetoedIngredients(id INT)
    LANGUAGE PLPGSQL
    AS $$
    BEGIN
      SELECT vetoIngredient FROM vetoedIngredients WHERE userId = id;
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

if __name__ == "__main__":
    createUserStoredProcedure()