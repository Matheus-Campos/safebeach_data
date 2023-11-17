from enum import Enum
import requests

from .exceptions.open_meteo_invalid_request import OpenMeteoInvalidRequest


class HourlyData(Enum):
    temperature = "temperature_2m"
    precipitation = "precipitation"
    rain = "rain"
    apparent_temperature = "apparent_temperature"
    wind_speed = "wind_speed_10m"


class OpenMeteoClient:
    __BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

    @staticmethod
    def get_data_from(lat, lng, start, end, hourly_data):
        try:
            response = requests.get(
                OpenMeteoClient.__BASE_URL,
                params={
                    "latitude": lat,
                    "longitude": lng,
                    "start_date": str(start),
                    "end_date": str(end),
                    "temperature_unit": "celsius",
                    "windspeed_unit": "kmh",
                    "precipitation_unit": "mm",
                    "timeformat": "iso8601",
                    "timezone": "America/Recife",
                    "hourly": [data.value for data in hourly_data],
                },
                headers={"Accept": "application/json"},
            )

            body = response.json()

            if body.get("error") == "True" or response.status_code >= 400:
                raise OpenMeteoInvalidRequest(body)

            return body
        except OpenMeteoInvalidRequest as e:
            print("Error occurred while requesting OpenMeteo:", e.args)
            return None
        except Exception as e:
            print("Error occurred while fetching data from OpenMeteo:", e.args)
            return None
