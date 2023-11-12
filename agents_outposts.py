import sys
import pandas as pd

import db

conn = None


def main():
    df = pd.read_excel("data/Postos de Guarda Vidas.xls", 0)
    for _, row in df.iterrows():
        insert_outpost_into_db(row)


def insert_outpost_into_db(outpost):
    cursor = conn.cursor()
    sql = f"""
    INSERT INTO agent_outposts (name, latitude, longitude, location) VALUES (
        '{outpost['IDENTIFICAÇÃO']}',
        {outpost['LATITUDE']},
        {outpost['LONGITUDE']},
        'POINT({outpost['LATITUDE']} {outpost['LONGITUDE']})'
    );
    """
    cursor.execute(sql)
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


def drop_table():
    cur = conn.cursor()
    drop_table = "DROP TABLE IF EXISTS agent_outposts;"

    cur.execute(drop_table)
    conn.commit()


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
