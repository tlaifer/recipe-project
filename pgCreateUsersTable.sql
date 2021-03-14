CREATE TABLE IF NOT EXISTS users(
    
    userId INT, 
    username varchar, 
    familarTechniques INT[], 
    vetoedTechniques INT[]

);

INSERT INTO users (userId, username, familarTechniques)
VALUES(1, 'TestUser', '{3, 6, 8}')

/* run psql recipe_dev --file pgCreateUsersTable.sql.*/