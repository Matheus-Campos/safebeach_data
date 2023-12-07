import json
import os
from datetime import datetime, date
import pytz

import dotenv
from api.tides.stormglass import StormglassClient


def main(stormglass):
    with open("shark_incidents.json", "r+") as file:
        shark_incidents = json.load(file)
        local_tz = pytz.timezone("America/Recife")
        stormglass_quota_exceeded = False

        for i in range(len(shark_incidents)):
            si = shark_incidents[i]
            progress = round((i + 1) / len(shark_incidents) * 100)

            def log_with_progress(msg):
                print("{}% - {}".format(progress, msg))

            if not stormglass_quota_exceeded and si["tides"] is None:
                log_with_progress(
                    "Checking shark incident %s for tides data" % si["id"]
                )
                si_date = date.fromisoformat(si["date"])
                tides = stormglass.get_data_from(
                    si["nearest_outpost"]["latitude"],
                    si["nearest_outpost"]["longitude"],
                    si_date,
                    si_date,
                ).get("data")

                if tides is not None:
                    for t in tides:
                        t["time"] = datetime.fromisoformat(t["time"]).astimezone(
                            local_tz
                        )

                    si["tides"] = tides
                    log_with_progress(
                        "Updated tides data for shark incident %s" % si["id"]
                    )
                else:
                    stormglass_quota_exceeded = True
                    log_with_progress(
                        "Stormglass returned null either because of daily quota or an unknown error"
                    )

                if stormglass_quota_exceeded:
                    break
            else:
                log_with_progress("Skipping shark incident %s" % si["id"])

        file.seek(0)
        file.truncate()
        json.dump(
            shark_incidents,
            file,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
            default=__serialize_time,
        )


def __serialize_time(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


if __name__ == "__main__":
    dotenv.load_dotenv()
    apikey = os.getenv("STORMGLASS_API_KEY")
    main(StormglassClient(apikey))
