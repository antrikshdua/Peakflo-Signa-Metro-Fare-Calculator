from fair_calculator.modules.v1.enums import fare_caps, fare_rules, peak_hours
from fair_calculator.modules.v1.schemas import Journey
from typing import List
from datetime import datetime

# async def calculate_fare(journeys: List[Journey]) -> int:
#     total_fare = 0
#     current_week = None
#     daily_usage = {}
#     weekly_usage = {}

#     for journey in journeys:
#         from_line = journey.from_line
#         to_line = journey.to_line
#         datetime = journey.datetime

#         # Check if it's a new week
#         # Keeps track of the current week to determine when to reset daily and weekly usage.
#         week_number = datetime.isocalendar()[1]
#         if week_number != current_week:
#             current_week = week_number
#             daily_usage = {}
#             weekly_usage = {}

#         # Calculate fare based on fare rules
#         fare_rule = fare_rules.get((from_line, to_line))
#         if not fare_rule:
#             return {"total_fare":f"Invalid Route {from_line} -> {to_line}"}
#             # raise HTTPException(status_code=400, detail="Invalid journey")

#         peak_hours = is_peak_hour(datetime)
#         fare = fare_rule.peak if peak_hours else fare_rule.non_peak

#         # Check and apply daily cap
#         daily_cap = fare_caps.get((from_line, to_line)).daily_cap
#         absolute_daily_usage = daily_usage.get(from_line, 0) + fare
#         if absolute_daily_usage > daily_cap:
#             # fare = daily_cap - daily_usage[from_line]
#             return {"total_fare": f"Your ride is free for today. Limit Exceeded for Route: {from_line.value} -> {to_line.value} Daily Limit: {daily_cap}, Fare: {absolute_daily_usage}"}

#         # Update daily usage
#         daily_usage[from_line] = daily_usage.get(from_line, 0) + fare

#         # # Check and apply weekly cap
#         # weekly_cap = fare_caps.get((from_line, to_line)).weekly_cap
#         # absolute_weekly_usage = weekly_usage.get(from_line, 0) + fare
#         # if absolute_weekly_usage > weekly_cap:
#         #         return {"total_fare":"Your ride is free this week"}

#         # Check and apply weekly cap
#         weekly_cap = fare_caps.get((from_line, to_line)).weekly_cap
#         weekly_usage[from_line] = weekly_usage.get(from_line, 0) + fare

#         if weekly_usage[from_line] > weekly_cap:
#             return {"total_fare": "Your ride is free this week"}

#         weekly_usage[from_line] = weekly_usage.get(from_line, 0) + fare

#         # Update total fare
#         total_fare += fare
#     print(f"Total Fare: {total_fare}, DailyUsage: {daily_usage}, WeeklyUsage: {weekly_usage}")
#     return {"total_fare": str(total_fare)+"$"}

# async def calculate_fare(journeys: List[Journey]) -> int:
#     total_fare = 0
#     current_week = None
#     daily_usage = {}
#     weekly_usage = {}

#     for journey in journeys:
#         from_line = journey.from_line
#         to_line = journey.to_line
#         datetime = journey.datetime

#         # Check if it's a new week
#         week_number = datetime.isocalendar()[1]
#         if week_number != current_week:
#             current_week = week_number
#             daily_usage = {}
#             weekly_usage = {}

#         # Calculate fare based on fare rules
#         fare_rule = fare_rules.get((from_line, to_line))
#         if not fare_rule:
#             return {"total_fare": f"Invalid Route {from_line} -> {to_line}"}

#         peak_hours = is_peak_hour(datetime)
#         fare = fare_rule.peak if peak_hours else fare_rule.non_peak

#         # Check and apply weekly cap
#         weekly_cap = fare_caps.get((from_line, to_line)).weekly_cap
#         absolute_weekly_usage = weekly_usage.get(from_line, 0) + fare
#         if absolute_weekly_usage > weekly_cap:
#             return {"total_fare": "Your ride is free this week"}

#         weekly_usage[from_line] = weekly_usage.get(from_line, 0) + fare

#         # Check and apply daily cap
#         daily_cap = fare_caps.get((from_line, to_line)).daily_cap
#         absolute_daily_usage = daily_usage.get(from_line, 0) + fare
#         if absolute_daily_usage > daily_cap:
#             fare = daily_cap - daily_usage[from_line]
#             return {
#                 "total_fare": f"Your ride is free for today. "
#                 f"Limit Exceeded for Route: {from_line} -> {to_line}, "
#                 f"Daily Limit: {daily_cap}, Fare: {absolute_daily_usage}"
#             }

#         # Update daily usage
#         daily_usage[from_line] = daily_usage.get(from_line, 0) + fare

#         # Update total fare
#         total_fare += fare

#     print(f"Total Fare: {total_fare}, Daily Usage: {daily_usage}, Weekly Usage: {weekly_usage}")
#     return {"total_fare": str(total_fare) + "$"}

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
            return {"total_fare": f"Invalid Route {from_line} -> {to_line}"}

        peak_hours = is_peak_hour(journey_datetime)
        fare = fare_rule.peak if peak_hours else fare_rule.non_peak

        # Check and apply daily cap
        daily_cap = fare_caps.get((from_line, to_line)).daily_cap
        weekly_cap = fare_caps.get((from_line, to_line)).weekly_cap
        
        # if from_line == to_line or from_line != to_line:
        #     if daily_usage.get(from_line, 0) + fare > daily_cap:
        #         fare = daily_cap - daily_usage[from_line] # In-order to stop the system from over chargig the user
        #         daily_usage[from_line] = daily_cap  # Mark the cap as reached
        # else:
        #     # Check if daily or weekly cap is exceeded
        #     if (daily_usage.get(from_line, 0) + fare > daily_cap) or \
        #        (weekly_usage.get(from_line, 0) + fare > weekly_cap):
        #         print("Your Ride is free")
        #         fare = 0  # Make the ride free
        total_daily_usage = daily_usage.get(from_line, 0) + fare
        total_weekly_usage = weekly_usage.get(from_line, 0) + fare
        if (total_daily_usage > daily_cap) or \
            (total_weekly_usage > weekly_cap):
                fare = daily_cap - daily_usage[from_line] # In-order to stop the system from over chargig the user
                daily_usage[from_line] = daily_cap  # Mark the cap as reached
                return {"total_fare": f"Your Ride is Free, Daily:{total_daily_usage > daily_cap}, Weekly:{total_weekly_usage > weekly_cap}"}
                fare = 0  # Make the ride free
        
        # Update daily usage
        daily_usage[from_line] = daily_usage.get(from_line, 0) + fare
        weekly_usage[from_line] = weekly_usage.get(from_line, 0) + fare

        # Update total fare
        total_fare += fare

    return {"total_fare": str(total_fare) + "$"}

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
    