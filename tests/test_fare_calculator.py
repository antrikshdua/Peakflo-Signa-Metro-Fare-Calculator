import pytest
from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

# Function to read the content of a CSV file
def read_csv_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Use the real CSV file from the folder
normal_fare_csv = read_csv_file("test-csv/normal-fare-calculation.csv")
invalid_route_csv = read_csv_file("test-csv/invalid-route-data.csv")
daily_limit_exceed_csv = read_csv_file("test-csv/daily-limit-exceeded.csv")
weekly_limit_exceed_csv = read_csv_file("test-csv/weekly-limit-exceeded.csv")

def test_normal_fare_calculation():
    response = client.post("/calculate-fare/", files={"file": ("test.csv", normal_fare_csv)})
    # assert response.status_code == 200
    assert response.json() == {
                                "message": "You have to pay",
                                "total_fare": "17$",
                                "daily_limit_exceed": False,
                                "weekly_limit_exceed": False
                            }  # Adjust the expected result based on your calculation

def test_invalid_csv_data():
    # Test with invalid CSV data
    response = client.post("/calculate-fare/", files={"file": ("test.csv", invalid_route_csv)})
    assert response.status_code == 400  
    assert response.json() == {
        'detail': 'Invalid Route Red -> Blue'
    }

def test_daily_limit_exceed():
    # Test with missing fields in CSV
    response = client.post("/calculate-fare/", files={"file": ("test.csv", daily_limit_exceed_csv)})
    assert response.status_code == 200  
    assert response.json() == {
                                "message": "Your Ride is Free",
                                "total_fare": "Null",
                                "daily_limit_exceed": True,
                                "weekly_limit_exceed": False
                            }

def test_weekly_limit_exceed():
    # Test with missing fields in CSV
    response = client.post("/calculate-fare/", files={"file": ("test.csv", weekly_limit_exceed_csv)})
    assert response.status_code == 200  
    assert response.json() == {
                                "message": "Your Ride is Free",
                                "total_fare": "Null",
                                "daily_limit_exceed": False,
                                "weekly_limit_exceed": True
                            }