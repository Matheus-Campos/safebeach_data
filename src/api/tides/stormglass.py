from datetime import datetime, time
import requests


class StormglassClient:
    __BASE_URL = "https://api.stormglass.io/v2/tide/extremes/point"

    def __init__(self, apikey):
        self.apikey = apikey

    def get_data_from(self, lat, lng, start, end):
        response = requests.get(
            self.__BASE_URL,
            params={
                "lat": lat,
                "lng": lng,
                "start": datetime.timestamp(datetime.combine(start, time.min)),
                "end": datetime.timestamp(datetime.combine(end, time.max)),
            },
            headers={"Authorization": self.apikey},
        )

        return response.json()
