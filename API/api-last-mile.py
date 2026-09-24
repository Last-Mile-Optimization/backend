import requests
import pandas as pd
from datetime import datetime
import time

API_KEY = "tc_live_EexgyctSB1KqBYBo0Ui7T39toZX-x9HdH9q5Ix6_9BU"

BASE_URL = "https://api.trackcourier.io/v1/track"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

tracking_list = [
    {
        "tracking_number": "AB123456789",
        "courier": "dhl",
        "expected_delivery_date": "2026-05-10"
    },
    {
        "tracking_number": "CD987654321",
        "courier": "fedex",
        "expected_delivery_date": "2026-05-08"
    }
]

results = []

for item in tracking_list:

    tracking_number = item["tracking_number"]
    courier = item["courier"]
    expected_date = item["expected_delivery_date"]

    params = {
        "courier": courier,
        "tracking_number": tracking_number
    }

    try:

        response = requests.get(
            BASE_URL,
            headers=headers,
            params=params,
            timeout=30
        )

        data = response.json()

        shipment = data.get("data", {})
        events = shipment.get("events", [])

        delivered_date = None
        last_status = None
        origin = None
        destination = None

        route_history = []

        for event in events:

            status = event.get("status")
            location = event.get("location")
            date = event.get("date")

            route_history.append(
                f"{date} - {location} - {status}"
            )

            if not origin and location:
                origin = location

            destination = location
            last_status = status

            if status and "delivered" in status.lower():
                delivered_date = date

        delayed = None

        if delivered_date and expected_date:

            expected_dt = datetime.strptime(
                expected_date,
                "%Y-%m-%d"
            )

            delivered_dt = datetime.strptime(
                delivered_date[:10],
                "%Y-%m-%d"
            )

            delayed = delivered_dt > expected_dt

        results.append({
            "tracking_number": tracking_number,
            "courier": courier,
            "current_status": last_status,
            "origin": origin,
            "destination": destination,
            "expected_delivery_date": expected_date,
            "delivered_date": delivered_date,
            "delayed": delayed,
            "total_events": len(events),
            "route_history": " | ".join(route_history)
        })

        print(f"Processed: {tracking_number}")

        time.sleep(1)

    except Exception as e:

        print(f"Error processing {tracking_number}: {e}")

output_df = pd.DataFrame(results)

output_df.to_csv(
    "deliveries_output.csv",
    index=False,
    encoding="utf-8-sig"
)

print("CSV generated successfully!")