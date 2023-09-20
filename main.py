from uvicorn import run
from fastapi import FastAPI, UploadFile, HTTPException
from fair_calculator.modules.v1.schemas import Journey, FareCalculation
from fair_calculator.modules.v1.business_logic import calculate_fare
from datetime import datetime
import csv

app = FastAPI()

@app.post("/calculate-fare", response_model=FareCalculation) #in-order to avoid redirection from root
@app.post("/calculate-fare/", response_model=FareCalculation)
async def calculate_fare_endpoint(file: UploadFile):
    try:
        # Read and parse the uploaded CSV file
        journeys = []
        content = await file.read()
        decoded_content = content.decode("utf-8").splitlines()
        csv_reader = csv.reader(decoded_content)

        for row in csv_reader:
            if len(row) == 3:
                from_line, to_line, datetime_str = row
                journey_datetime = datetime.fromisoformat(datetime_str)
                journeys.append(Journey(from_line=from_line, to_line=to_line, datetime=journey_datetime))

        # # Calculate the total fare
        total_fare = await calculate_fare(journeys)
        return total_fare

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000)