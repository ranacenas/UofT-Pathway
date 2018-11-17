import psycopg2
from config import config


def create_tables():
    commands = ("""
        CREATE TABLE IF NOT EXISTS Course (cID VARCHAR(30) NOT NULL, cName\
        VARCHAR(300) NOT NULL, credits FLOAT NOT NULL, campus VARCHAR(150) NOT NULL,\
        department VARCHAR(160) NOT NULL, term VARCHAR(150) NOT NULL, division\
        VARCHAR(200) NOT NULL, prerequisites VARCHAR(1000), exclusion VARCHAR(1000), br\
        VARCHAR(200), lecNum VARCHAR(30) NOT NULL, lecTime VARCHAR(125) NOT\
        NULL, instructor VARCHAR(500), location VARCHAR(250), size INT(5),\
        currentEnrollment INT(5), PRIMARY KEY (cID, term, lecNum)) CHARACTER SET=utf8"
        """)
    
    conn = None
    try:
        params = config()

        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(commands)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__=='__main__':
    create_tables()