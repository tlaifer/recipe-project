import psycopg2

postgres_connection = psycopg2.connect(dbname="recipe_dev", user="postgres", password="postgres")