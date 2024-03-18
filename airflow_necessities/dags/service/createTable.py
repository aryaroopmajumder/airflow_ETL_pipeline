from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

def make_database():
    """
    Make the Postgres database and create the table.
    """

    host_name = 'HOSTNAME'
    database = 'DB_NAME'
    user = 'USERNAME'
    password = 'PASSWORD'
    table = 'TABLE'

    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host_name}/{database}')

    if not database_exists(engine.url):
        create_database(engine.url)

    conn = psycopg2.connect(database = dbname, user = username)

    curr = conn.cursor()

    create_table = """CREATE TABLE IF NOT EXISTS %s
                (
                    city         TEXT, 
                    country      TEXT,
                    latitude     REAL,
                    longitude    REAL,
                    todays_date  DATE,
                    humidity     REAL,
                    pressure     REAL,
                    min_temp     REAL,
                    max_temp     REAL,
                    temp         REAL,
                    weather      TEXT
                )
                """ % tablename

    curr.execute(create_table)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    make_database()