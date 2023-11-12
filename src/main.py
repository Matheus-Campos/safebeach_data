from datetime import date, timedelta
import json

import numpy as np
import db
from weather_api.openmeteo import HourlyData, OpenMeteoClient


def main():
    with db.connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, latitude, longitude FROM agent_outposts;")
        outposts = [build_outpost(data) for data in cur.fetchall()]

        cur.execute(
            "SELECT id, victim_survived, date, moon_phase, wound, next_to, beach, city FROM shark_incidents;"
        )
        incidents = [build_incident(data) for data in cur.fetchall()]

    piedade_outpost = [o for o in outposts if o["name"].find("Igrejinha") != -1].pop()
    print("Posto da igrejinha:", piedade_outpost["name"])

    igrejinha_incidents = [i for i in incidents if i["next_to"] == "Igreja de Piedade"]
    print(f"{len(igrejinha_incidents)} incidentes na igrejinha")

    data = [
        get_shark_incident_data(igrejinha_incidents, i, piedade_outpost)
        for i in range(len(igrejinha_incidents))
    ]

    with open("shark_incidents.json", "w") as file:
        json.dump(data, file, indent=2, default=serialize_time, ensure_ascii=False)


def serialize_time(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def get_shark_incident_data(incidents, index, outpost):
    incident = incidents[index]
    progress = round((index + 1) / len(incidents) * 100)
    print(f"Pegando dados meteorológicos do incidente {incident['id']}... {progress}%")

    incident_date = incident["date"]
    response = OpenMeteoClient.get_data_from(
        outpost["lat"],
        outpost["lng"],
        incident_date - timedelta(days=1),
        incident_date,
        [
            HourlyData.rain,
            HourlyData.temperature,
            HourlyData.precipitation,
            HourlyData.apparent_temperature,
            HourlyData.wind_speed,
        ],
    )

    return {
        "previous_day_weather": hourly_to_daily_data(response["hourly"], 0, 24),
        "incident_day_weather": hourly_to_daily_data(response["hourly"], 24, 48),
        **incident,
    }


def hourly_to_daily_data(hourly, start, end):
    return {
        "rain_sum_in_mm": round(np.sum(hourly[HourlyData.rain.value][start:end]), 2),
        "precipitation_sum_in_mm": round(
            np.sum(hourly[HourlyData.precipitation.value][start:end]), 2
        ),
        "temperature_avg_in_c": round(
            np.average(hourly[HourlyData.temperature.value][start:end]), 2
        ),
        "apparent_temperature_avg_in_c": round(
            np.average(hourly[HourlyData.apparent_temperature.value][start:end]),
            2,
        ),
        "wind_speed_avg_in_kmh": round(
            np.average(hourly[HourlyData.wind_speed.value][start:end]), 2
        ),
    }


def build_outpost(data):
    return {
        "id": data[0],
        "name": data[1],
        "lat": data[2],
        "lng": data[3],
    }


def build_incident(data):
    return {
        "id": data[0],
        "victim_survived": data[1],
        "date": data[2],
        "moon_phase": data[3],
        "wound": data[4],
        "next_to": data[5],
        "beach": data[6],
        "city": data[7],
    }


if __name__ == "__main__":
    main()
