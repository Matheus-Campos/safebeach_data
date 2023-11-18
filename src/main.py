from datetime import date, datetime, timedelta
from time import time
import json
import os
import pytz

import numpy as np
from api.geocoding.google import GoogleMapsClient
import db
from dotenv import load_dotenv
from api.weather.openmeteo import HourlyData, OpenMeteoClient
from api.tides.stormglass import StormglassClient
from queries import SELECT_NEAREST_AGENT_OUTPOST, SELECT_SHARK_INCIDENTS


class Main:
    __LOCAL_TZ = pytz.timezone("America/Recife")

    def __init__(self, dbConn, stormglass, googlemaps):
        self.dbConn = dbConn
        self.stormglass = stormglass
        self.googlemaps = googlemaps

    def get_raw_incidents_from_db(self):
        cur = self.dbConn.cursor()
        cur.execute(SELECT_SHARK_INCIDENTS)
        incidents = [self.__build_incident(data) for data in cur.fetchall()]
        cur.close()

        return incidents

    def main(self):
        incidents = self.get_raw_incidents_from_db()

        data = [self.improve_incident_data(incidents, i) for i in range(len(incidents))]

        with open("shark_incidents.json", "w") as file:
            json.dump(
                data,
                file,
                indent=2,
                default=self.__serialize_time,
                ensure_ascii=False,
                sort_keys=True,
            )

    def __serialize_time(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        raise TypeError("Type not serializable")

    def improve_incident_data(self, incidents, index):
        progress = round((index) / len(incidents) * 100)
        print(f"\nProgresso: {progress}%")

        incident = incidents[index]
        print("Pegando coordenadas geográficas do incidente %s" % incident["id"])

        approx_location = self.googlemaps.geocode(incident)
        if approx_location is None:
            print(
                'Não foi possível achar coordenadas geográficas para "%s"'
                % incident["next_to"]
            )
        else:
            print(
                "Coordenadas aproximadas: Latitude %f, Longitude: %f"
                % (approx_location["lat"], approx_location["lng"])
            )
            cursor = self.dbConn.cursor()
            cursor.execute(
                SELECT_NEAREST_AGENT_OUTPOST,
                (approx_location["lng"], approx_location["lat"]),
            )
            nearest_outpost = self.__build_outpost(cursor.fetchone())
            cursor.close()

            print(
                "Posto guarda-vidas mais próximo: %s\nDistância aproximada do incidente %.2fm"
                % (nearest_outpost["name"], nearest_outpost["distance_to_incident"])
            )

            print("Pegando dados meteorológicos do incidente %s..." % incident["id"])

            incident_date = incident["date"]
            weather = OpenMeteoClient.get_data_from(
                nearest_outpost["latitude"],
                nearest_outpost["longitude"],
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

            print("Pegando dados de maré no dia %s" % incident_date.isoformat())

            tides = self.stormglass.get_data_from(
                nearest_outpost["latitude"],
                nearest_outpost["longitude"],
                incident_date,
                incident_date,
            ).get("data")

            for tide in tides:
                tide["time"] = datetime.fromisoformat(tide["time"]).astimezone(
                    self.__LOCAL_TZ
                )

            return {
                "previous_day_weather": self.__hourly_to_daily_data(
                    weather["hourly"], 0, 24
                ),
                "incident_day_weather": self.__hourly_to_daily_data(
                    weather["hourly"], 24, 48
                ),
                "nearest_outpost": nearest_outpost,
                "tides": tides,
                **incident,
            }

    def __hourly_to_daily_data(self, hourly, start, end):
        return {
            "rain_sum_in_mm": round(
                np.sum(hourly[HourlyData.rain.value][start:end]), 2
            ),
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

    def __build_outpost(self, data):
        return {
            "name": data[0],
            "latitude": data[1],
            "longitude": data[2],
            "distance_to_incident": data[3],
        }

    def __build_incident(self, data):
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
    load_dotenv()
    stormglass = StormglassClient(os.getenv("STORMGLASS_API_KEY"))
    googlemaps = GoogleMapsClient(os.getenv("GOOGLE_MAPS_API_KEY"))
    start = time()
    with db.connect() as conn:
        Main(conn, stormglass, googlemaps).main()
    end = time()
    print("Coleta de dados levou %ss para finalizar" % (end - start))
