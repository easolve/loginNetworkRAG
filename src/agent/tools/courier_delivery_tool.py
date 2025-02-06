from langchain.tools import tool
from typing import Dict
from os import getenv
import requests
from datetime import datetime, timezone


@tool
def courier_delivery_tool(waybill_number: str) -> Dict:
    """
    운송장 번호를 통해서 택배 배송 정보를 제공합니다.
    - time: 택배 배송 완료 시간
    - status: 택배 배송 상태

    Returns:
        Dict: {
            "time": str,
            "status": str,
        }
    """
    print(waybill_number)

    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00Z")

    track_response = requests.post(
        url="https://apis.tracker.delivery/graphql",
        headers={
            "Authorization": (
                f"TRACKQL-API-KEY {getenv('TRACKQL_CLIENT_ID')}:{getenv('TRACKQL_CLIENT_SECRET')}"
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
            "variables": {
                "carrierId": "dev.track.dummy",
                "trackingNumber": current_time,
            },
        },
    ).json()

    last_event = track_response.get("data", {}).get("track", {}).get("lastEvent", {})
    time = last_event.get("time", "정보 없음")
    status = last_event.get("status", {}).get("code", "정보 없음")
    return {"time": time, "status": status}
