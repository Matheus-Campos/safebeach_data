import json
from datetime import datetime
import pytz


def main():
    with open("shark_incidents.json", "r+") as file:
        incidents = json.load(
            file,
        )
        local_tz = pytz.timezone("America/Recife")
        for incident in incidents:
            if incident["tides"] is None:
                continue

            for tide in incident["tides"]:
                dt = datetime.fromisoformat(tide["time"]).astimezone(local_tz)
                tide["time"] = dt

        file.seek(0)
        file.truncate()
        json.dump(
            incidents,
            file,
            default=__serialize_time,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )


def __serialize_time(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


if __name__ == "__main__":
    main()
