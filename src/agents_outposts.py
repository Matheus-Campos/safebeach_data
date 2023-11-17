import sys
import pandas as pd

import db as db
from queries import (
    CREATE_AGENT_OUTPOSTS_TABLE,
    DROP_AGENT_OUTPOSTS_TABLE,
    INSERT_AGENT_OUTPOST,
)

conn = None


def main():
    df = pd.read_excel("data/Postos de Guarda Vidas.xls", 0)
    for name, latitude, longitude in zip(
        df["IDENTIFICAÇÃO"], df["LATITUDE"], df["LONGITUDE"]
    ):
        insert_outpost_into_db(name, latitude, longitude)


def insert_outpost_into_db(name, latitude, longitude):
    cursor = conn.cursor()
    cursor.execute(
        INSERT_AGENT_OUTPOST,
        (name, latitude, longitude, f"POINT({longitude} {latitude})"),
    )
    conn.commit()


def create_table_if_not_exists():
    cur = conn.cursor()
    cur.execute(CREATE_AGENT_OUTPOSTS_TABLE)
    conn.commit()
    conn.close()


def drop_table():
    cur = conn.cursor()
    cur.execute(DROP_AGENT_OUTPOSTS_TABLE)
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
