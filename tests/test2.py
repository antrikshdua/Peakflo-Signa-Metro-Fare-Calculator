import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Sample CSV data for testing
sample_csv_data = "Green,Red,2021-03-24T07:58:30\nRed,Red,2021-03-25T11:58:30"

def test_calculate_fare():
    response = client.post("/calculate-fare/", files={"file": ("test.csv", sample_csv_data)})
    assert response.status_code == 200
    assert response.json() == {"total_fare": 10}  # Adjust the expected result based on your calculation

def test_calculate_fare_invalid_csv():
    # Test with invalid CSV data
    invalid_csv_data = "Invalid,Data,2021-03-24T07:58:30"
    response = client.post("/calculate-fare/", files={"file": ("test.csv", invalid_csv_data)})
    assert response.status_code == 400
    assert "Invalid CSV format" in response.text

def test_calculate_fare_missing_fields():
    # Test with missing fields in CSV
    missing_fields_csv = "Green,2021-03-24T07:58:30"
    response = client.post("/calculate-fare/", files={"file": ("test.csv", missing_fields_csv)})
    assert response.status_code == 400
    assert "CSV must have exactly 3 fields" in response.text