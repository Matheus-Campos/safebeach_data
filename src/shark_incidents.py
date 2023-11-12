import datetime as dt
import sys
import pandas as pd

import db as db

conn = None

MOON_PHASES = {"Ch": "full", "Nv": "new", "Mg": "waning", "Cr": "waxing"}
MONTHS = [
    "JAN",
    "FEV",
    "MAR",
    "ABR",
    "MAI",
    "JUN",
    "JUL",
    "AGO",
    "SET",
    "OUT",
    "NOV",
    "DEZ",
]


def main():
    file_path = "data/ESTATÍSTICA 67º INCIDENTE - CONTINENTE (SITE - INICIAIS).xlsx"
    start, end = 8, 75
    columns = [
        "id",
        "is_alive",
        "role",
        "date",
        "month",
        "year",
        "day_of_week",
        "name",
        "age",
        "sex",
        "place",
        "moon_phase",
        "wound",
        "beach",
        "city",
    ]
    relevant_columns = [
        "is_alive",
        "date",
        "month",
        "year",
        "place",
        "wound",
        "moon_phase",
        "beach",
        "city",
    ]
    df = pd.read_excel(
        file_path, "dados", keep_default_na=False, header=None, names=columns
    )[start:end]

    for (
        is_alive,
        date,
        month,
        year,
        place,
        wound,
        moon_phase,
        beach,
        city,
    ) in zip(*[df[column] for column in relevant_columns]):
        incident = {
            "victim_survived": is_alive,
            "date": dt.date(year, MONTHS.index(month) + 1, date),
            "moon_phase": MOON_PHASES[moon_phase],
            "wound": wound,
            "next_to": place,
            "beach": beach,
            "city": city,
        }
        insert_incident_into_db(incident)


def insert_incident_into_db(incident):
    cur = conn.cursor()
    sql = "INSERT INTO shark_incidents (victim_survived, date, moon_phase, wound, next_to, beach, city) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cur.execute(
        sql,
        (
            bool(incident["victim_survived"]),
            incident["date"],
            incident["moon_phase"],
            incident["wound"],
            incident["next_to"],
            incident["beach"],
            incident["city"],
        ),
    )
    conn.commit()


def create_table_if_not_exists():
    cur = conn.cursor()

    create_types = "CREATE TYPE moon_phase AS ENUM ('new', 'waxing', 'full', 'waning');"

    cur.execute(create_types)

    create_table = """
    CREATE TABLE IF NOT EXISTS shark_incidents (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        victim_survived BOOLEAN DEFAULT true,
        date DATE NOT NULL,
        moon_phase moon_phase NOT NULL,
        wound VARCHAR(255),
        next_to VARCHAR(255),
        beach VARCHAR(255) NOT NULL,
        city VARCHAR(255) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT now(),
        updated_at TIMESTAMP NOT NULL DEFAULT now()
    );
    """

    cur.execute(create_table)
    conn.commit()
    conn.close()


def drop_table_if_exists():
    cur = conn.cursor()

    drop_table = "DROP TABLE IF EXISTS shark_incidents;"
    cur.execute(drop_table)
    drop_type = "DROP TYPE IF EXISTS moon_phase;"
    cur.execute(drop_type)
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
        drop_table_if_exists()
    elif migration is None:
        main()
