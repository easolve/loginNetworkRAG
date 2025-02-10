from datetime import datetime, timezone
from os import getenv

import requests
from dotenv import load_dotenv

load_dotenv()

current_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00Z")

track_response = requests.post(
    url="https://apis.tracker.delivery/graphql",
    headers={
        "Authorization": (
            f"TRACKQL-API-KEY {getenv("TRACKQL_CLIENT_ID")}:{getenv("TRACKQL_CLIENT_SECRET")}"
        ),
    },
    json={
        "query": (
            """
query Track(
  $carrierId: ID!,
  $trackingNumber: String!
) {
  track(
    carrierId: $carrierId,
    trackingNumber: $trackingNumber
  ) {
    lastEvent {
      time
      status {
        code
      }
    }
  }
}
""".strip()
        ),
        "variables": {"carrierId": "dev.track.dummy", "trackingNumber": current_time},
    },
).json()

print(track_response)
