import requests


class GoogleMapsClient:
    __BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
    __BOUNDS_NE_LAT, __BOUNDS_NE_LNG = -7.607942, -34.809841
    __BOUNDS_SO_LAT, __BOUNDS_SO_LNG = -8.348420, -34.974928

    def __init__(self, apikey):
        self.apikey = apikey

    def geocode(self, incident):
        response = requests.get(
            self.__BASE_URL,
            params={
                "bounds": f"{self.__BOUNDS_NE_LAT},{self.__BOUNDS_NE_LNG}|{self.__BOUNDS_SO_LAT},{self.__BOUNDS_SO_LNG}",
                "address": "%s %s %s"
                % (incident["next_to"], incident["beach"], incident["city"]),
                "language": "pt-BR",
                "key": self.apikey,
            },
        )

        if not response.ok:
            return None

        body = response.json()
        if body["status"] != "OK":
            return None

        return body["results"][0]["geometry"]["location"]
