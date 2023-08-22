import psycopg2

def create_table():
    command = (
        """
        CREATE TABLE users (
            username VARCHAR(255) NOT NULL PRIMARY KEY,
            passwordHash VARCHAR(255) NOT NULL,
            randomVal INTEGER NOT NULL,
            secID VARCHAR(255) NOT NULL,
            qrimage BYTEA,
            sqrimage BYTEA
        )
        """
    )
    conn = None 
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="postgres"
        )
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_table()