import datetime as dt
import sys
import pandas as pd

import db as db
from queries import (
    CREATE_MOON_PHASE_TYPE,
    CREATE_SHARK_INCIDENTS_TABLE,
    DROP_MOON_PHASE_TYPE,
    DROP_SHARK_INCIDENTS_TABLE,
    INSERT_SHARK_INCIDENT,
)

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
            "victim_survived": is_alive == "V",
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
    cur.execute(
        INSERT_SHARK_INCIDENT,
        (
            incident["victim_survived"],
            incident["date"],
            incident["moon_phase"],
            incident["wound"],
            incident["next_to"] if incident["next_to"] != "?" else None,
            incident["beach"],
            incident["city"],
        ),
    )
    conn.commit()


def create_table_if_not_exists():
    cur = conn.cursor()
    cur.execute(CREATE_MOON_PHASE_TYPE)
    cur.execute(CREATE_SHARK_INCIDENTS_TABLE)
    conn.commit()
    conn.close()


def drop_table_if_exists():
    cur = conn.cursor()
    cur.execute(DROP_SHARK_INCIDENTS_TABLE)
    cur.execute(DROP_MOON_PHASE_TYPE)
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
