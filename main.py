from uvicorn import run
from fastapi import FastAPI, UploadFile, HTTPException
from app.modules.v1.schemas import ResponseFareCalculation
from app.modules.v1.business_logic import calculate_fare
from app.core.utils import get_journeys_from_csv

app = FastAPI()

@app.post("/calculate-fare", response_model=ResponseFareCalculation) #in-order to avoid redirection from root
@app.post("/calculate-fare/", response_model=ResponseFareCalculation)
async def calculate_fare_endpoint(file: UploadFile):
    try:
        content = await file.read()
        journeys = get_journeys_from_csv(content=content)
        
        # # Calculate the total fare
        total_fare = await calculate_fare(journeys)
        return total_fare
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000)