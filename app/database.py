import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

# table_setup below is the main function which creates the posts & users tables

def table_setup():

    # Getting the posts table
    posts_table()

    # Getting the users table
    users_table()

    # Getting the votes table
    votes_table()

# Database credentials
# Note: 'fastapi' database already created beforehand using psql
def db_credentials():

    dbname = settings.database_name
    host = settings.database_hostname
    username = settings.database_username 
    pwd = settings.database_password
    port = settings.database_port

    return dbname, host, username, pwd, port

# Getting global variables con and cur

def setup_connection():

    dbname = db_credentials()[0]
    host = db_credentials()[1]
    username = db_credentials()[2]
    pwd = db_credentials()[3]
    port = db_credentials()[4]

    con = psycopg2.connect(database = dbname, host = host, user = username, password = pwd, port = port)
    
    return con

# Creating posts table inside fatsapi db
def posts_table():

    con = setup_connection()
    cur = con.cursor(cursor_factory=RealDictCursor)
    
    posts = cur.execute("""CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY, 
                title VARCHAR NOT NULL, 
                content TEXT NOT NULL, 
                published BOOL DEFAULT TRUE, 
                created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                user_id INT NOT NULL,
                CONSTRAINT fk_user_id
                    FOREIGN KEY(user_id)
                        REFERENCES users(id)
                            ON DELETE CASCADE
                )
                """)
    con.commit()
    return posts

# Creating posts table inside fatsapi db
def users_table():

    con = setup_connection()
    cur = con.cursor(cursor_factory=RealDictCursor)

    users = cur.execute("""CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY, 
                email VARCHAR NOT NULL UNIQUE, 
                password VARCHAR NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                )
                """)
    con.commit()
    return users

# Creating votes table inside fatsapi db
def votes_table():

    con = setup_connection()
    cur = con.cursor(cursor_factory=RealDictCursor)

    votes = cur.execute("""CREATE TABLE IF NOT EXISTS votes (
                post_id INT NOT NULL, 
                user_id INT NOT NULL,
                PRIMARY KEY(post_id,user_id),
                CONSTRAINT fk_votes_posts
                    FOREIGN KEY(post_id)
                        REFERENCES posts(id)
                            ON DELETE CASCADE,
                CONSTRAINT fk_votes_users
                    FOREIGN KEY(user_id)
                        REFERENCES users(id)
                            ON DELETE CASCADE
                )
                """)
    con.commit()
    return votes