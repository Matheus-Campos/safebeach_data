import sys
import pandas as pd

import db as db

conn = None


def main():
    df = pd.read_excel("data/Postos de Guarda Vidas.xls", 0)
    for name, latitude, longitude in zip(
        df["IDENTIFICAÇÃO"], df["LATITUDE"], df["LONGITUDE"]
    ):
        insert_outpost_into_db(name, latitude, longitude)


def insert_outpost_into_db(name, latitude, longitude):
    cursor = conn.cursor()
    sql = "INSERT INTO agent_outposts (name, latitude, longitude, location) VALUES (%s, %s, %s, %s);"
    cursor.execute(sql, (name, latitude, longitude, f"POINT({latitude} {longitude})"))
    conn.commit()


def create_table_if_not_exists():
    cur = conn.cursor()
    create_table = """
    CREATE TABLE IF NOT EXISTS agent_outposts (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR(255) NOT NULL,
        location geography(Point, 4326) NOT NULL,
        latitude DOUBLE PRECISION NOT NULL,
        longitude DOUBLE PRECISION NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT now(),
        updated_at TIMESTAMP NOT NULL DEFAULT now()
    )
    """

    cur.execute(create_table)
    conn.commit()
    conn.close()


def drop_table():
    cur = conn.cursor()
    drop_table = "DROP TABLE IF EXISTS agent_outposts;"

    cur.execute(drop_table)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    conn = db.connect()

    migration = None
    if len(sys.argv) > 1:
        migration = sys.argv[1]

    if migration == "up":
        create_table_if_not_exists()
    elif migration == "down":
        drop_table()
    elif migration is None:
        main()
