from pydantic import BaseModel
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

class FareCalculation(BaseModel):
    total_fare: str