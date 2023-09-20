import io
import pytest
from fastapi.testclient import TestClient
from main import app

# Define some sample user routes
sample_journeys = [
    {"from_line": "Green", "to_line": "Green", "datetime": "2023-07-10T09:30:00"},
    {"from_line": "Green", "to_line": "Red", "datetime": "2023-07-11T08:30:00"},
    {"from_line": "Red", "to_line": "Green", "datetime": "2023-07-12T18:30:00"},
]

# Mock the enum data
fare_rules = {
    ("Green", "Green"): {"non_peak": 1, "peak": 2},
    ("Red", "Red"): {"non_peak": 2, "peak": 3},
    ("Green", "Red"): {"non_peak": 3, "peak": 4},
    ("Red", "Green"): {"non_peak": 2, "peak": 3},
}

fare_caps = {
    ("Green", "Green"): {"daily_cap": 8, "weekly_cap": 55},
    ("Red", "Red"): {"daily_cap": 12, "weekly_cap": 70},
    ("Green", "Red"): {"daily_cap": 15, "weekly_cap": 90},
    ("Red", "Green"): {"daily_cap": 15, "weekly_cap": 90},
}

# Define test cases
@pytest.mark.parametrize("journeys, expected_fare", [
    (sample_journeys[:1], 2),  # Green to Green (Non-Peak)
    (sample_journeys[1:2], 12),  # Green to Red (Peak)
    (sample_journeys[2:], 12),  # Red to Green (Peak)
    (sample_journeys, 15),  # A combination of journeys (Should not exceed daily cap)
    ([sample_journeys[1]] * 8, 12),  # Exceed daily cap but stay within weekly cap
    ([sample_journeys[1]] * 13, 0),  # Exceed both daily and weekly caps (Ride should be free)
])
def test_calculate_fare(journeys, expected_fare):
    with TestClient(app) as client:
        # Create a CSV string from the sample journeys
        csv_data = "\n".join([f"{j['from_line']},{j['to_line']},{j['datetime']}" for j in journeys])
        
        # Convert the CSV string to bytes
        csv_bytes = csv_data.encode('utf-8')
        
        # Create a BytesIO object from the CSV bytes
        csv_file = io.BytesIO(csv_bytes)
        
        # Send a POST request with the CSV file
        response = client.post("/calculate-fare", files={"file": ("journeys.csv", csv_file)})
        
        # Check if the response status code is 200 OK
        assert response.status_code == 200
        
        # Parse the JSON response
        response_data = response.json()
        
        # Check if the total fare matches the expected fare
        assert response_data["total_fare"] == f"{expected_fare}$"

if __name__ == "__main__":
    pytest.main(["-vv"])





