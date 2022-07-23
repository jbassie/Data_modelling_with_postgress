from pickle import TRUE
import psycopg2
from sql_queries import create_table_queries,drop_table_queries

def create_database():
    """
    Create and connects to the sparkifydb database
    Return the conn and cursor to the database
    """
    #connect to default database
    conn = psycopg2.connect("host = localhost user = postgres password = 9507024922 dbname = udacity")
    conn.set_session(autocommit= TRUE)
    cur = conn.cursor()



    #Create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH encoding 'utf8' TEMPLATE \
        template0")
    
    #close the connection to default database
    conn.close()

    #connect to the default database
    conn = psycopg2.connect("host = localhost user = postgres password = 9507024922 dbname = sparkifydb")
    cur = conn.cursor()

    return cur, conn

def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list

    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and create the sparkify database.

    - Establishes connection with the sparkify database and gets cursor to it.

    - Drops all the tables

    - creates all tables needed.

    - Finally, closes the connection

    """
    cur, conn = create_database()
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()

if __name__ == "__main__":
    main()