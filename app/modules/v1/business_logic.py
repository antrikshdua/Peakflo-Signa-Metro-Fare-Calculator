from app.modules.v1.enums import fare_caps, fare_rules, peak_hours
from app.modules.v1.schemas import Journey, ResponseFareCalculation
from typing import List
from datetime import datetime
from fastapi import HTTPException

async def calculate_fare(journeys: List[Journey]) -> int:
    total_fare = 0
    current_week = None
    current_day = None
    daily_usage = {}
    weekly_usage = {}

    for journey in journeys:
        from_line = journey.from_line
        to_line = journey.to_line
        journey_datetime = journey.datetime

        # Check if it's a new week
        week_number = journey_datetime.isocalendar()[1]
        if week_number != current_week:
            current_week = week_number
            daily_usage = {}

        # Check if it's a new day
        day = journey_datetime.date()
        if day != current_day:
            current_day = day
            daily_usage = {}

        # Calculate fare based on fare rules
        fare_rule = fare_rules.get((from_line, to_line))
        if not fare_rule:
            message = f"Invalid Route {from_line} -> {to_line}"
            raise HTTPException(
                status_code=400,
                detail=str(message)
            )

        peak_hours = is_peak_hour(journey_datetime)
        fare = fare_rule.peak if peak_hours else fare_rule.non_peak

        # Check and apply daily cap
        daily_cap = fare_caps.get((from_line, to_line)).daily_cap
        weekly_cap = fare_caps.get((from_line, to_line)).weekly_cap
        
        total_daily_usage = daily_usage.get(from_line, 0) + fare
        total_weekly_usage = weekly_usage.get(from_line, 0) + fare
        if (total_daily_usage > daily_cap) or \
            (total_weekly_usage > weekly_cap):
                fare = daily_cap - daily_usage[from_line] # In-order to stop the system from over chargig the user
                daily_usage[from_line] = daily_cap  # Mark the cap as reached
                return ResponseFareCalculation(
                    message="Your Ride is Free",
                    daily_limit_exceed=total_daily_usage > daily_cap,
                    weekly_limit_exceed=total_weekly_usage > weekly_cap
                    )
        # Update daily and weekly usage
        daily_usage[from_line] = daily_usage.get(from_line, 0) + fare
        weekly_usage[from_line] = weekly_usage.get(from_line, 0) + fare

        # Update total fare
        total_fare += fare

    return ResponseFareCalculation(
            message="You have to pay",
            total_fare=str(total_fare) + "$",
            daily_limit_exceed=total_daily_usage > daily_cap,
            weekly_limit_exceed=total_weekly_usage > weekly_cap
        )

def is_peak_hour(datetime_obj: datetime) -> bool:
    # Get the day of the week (0 = Monday, 6 = Sunday)
    day_of_week = datetime_obj.weekday()

    # Get the time as (hour, minute)
    time = (datetime_obj.hour, datetime_obj.minute)

    # Check if the current time falls within any of the peak hour ranges
    if day_of_week < 5:  # Weekdays (Monday to Friday), Monday Starts from Zero
        peak_times = peak_hours["Weekday"]
    elif day_of_week == 5:  # Saturday
        peak_times = peak_hours["Saturday"]
    else:  # Sunday
        peak_times = peak_hours["Sunday"]

    for start_hour, start_minute, end_hour, end_minute in peak_times:
        start_time = (start_hour, start_minute)
        end_time = (end_hour, end_minute)
        if start_time <= time <= end_time:
            return True #Peak

    return False #Non-Peak
    