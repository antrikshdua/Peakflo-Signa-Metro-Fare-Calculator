import csv
from datetime import datetime, timedelta
from app.modules.v1.schemas import Journey 

# Define a function to generate journeys for a specific route that will exceed the weekly cap
def generate_journeys_to_exceed_weekly_cap(route, weekly_cap):
    journeys = []
    current_datetime = datetime(2023, 7, 10, 9, 30)  # Start on a Monday
    fare_per_trip = 5  # Adjust this to your fare rules

    # Create enough journeys to exceed the weekly cap
    while True:
        if len(journeys) >= weekly_cap // fare_per_trip:
            break

        # Create a journey for the specified route
        journeys.append({"from_line": route[0], "to_line": route[1], "datetime": current_datetime})

        # Increment the datetime to simulate a daily journey
        current_datetime += timedelta(days=1)
    print(journeys)
    return journeys

def get_journeys_from_csv(content):
    # Read and parse the uploaded CSV file
    journeys = []
    decoded_content = content.decode("utf-8").splitlines()
    csv_reader = csv.reader(decoded_content)

    for row in csv_reader:
        if len(row) == 3:
            from_line, to_line, datetime_str = row
            journey_datetime = datetime.fromisoformat(datetime_str)
            journeys.append(Journey(from_line=from_line, to_line=to_line, datetime=journey_datetime))

    return journeys
