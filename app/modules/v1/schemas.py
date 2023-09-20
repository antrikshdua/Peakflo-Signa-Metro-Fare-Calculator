from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class Line(str, Enum):
    Green = "Green"
    Red = "Red"
    Blue = "Blue"


class Journey(BaseModel):
    from_line: Line
    to_line: Line
    datetime: datetime

class FareCaps(BaseModel):
    daily_cap: int
    weekly_cap: int

class FareRules(BaseModel):
    non_peak: int
    peak: int

class ResponseFareCalculation(BaseModel):
    message: str
    total_fare: str = Field("Null", description="Message when nothing is calculated")
    daily_limit_exceed: bool = Field(False)
    weekly_limit_exceed: bool= Field(False)
