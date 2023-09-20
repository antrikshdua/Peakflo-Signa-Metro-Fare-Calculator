from app.modules.v1.schemas import Line, FareRules, FareCaps

"""
    All this data can be later on loaded from the cache/database
"""

# Load fare rules and caps from configuration
# Fares
# | FromLine | ToLine | Non-Peak| Peak|
# |----------|--------|----------|-----------|
# | Green    | Green  | 1       | 2        |
# | Red      | Red    | 2       | 3       |
# | Green    | Red    | 3       | 4        |
# | Red      | Green  | 2       | 3        |
fare_rules = {
    (Line.Green, Line.Green): FareRules(non_peak=1, peak=2),
    (Line.Red, Line.Red): FareRules(non_peak=2, peak=3),
    (Line.Green, Line.Red): FareRules(non_peak=3, peak=4),
    (Line.Red, Line.Green): FareRules(non_peak=2, peak=3),
}

#Caps
# | FromLine | ToLine | DailyCap | WeeklyCap |
# |-----------|---------|-----------|------------|
# | Green     | Green   | 8         | 55         |
# | Red       | Red     | 12        | 70         |
# | Green     | Red     | 15        | 90         |
# | Red       | Green   | 15        | 90         |
fare_caps = {
    (Line.Green, Line.Green): FareCaps(daily_cap=8, weekly_cap=55),
    (Line.Red, Line.Red): FareCaps(daily_cap=12, weekly_cap=70),
    (Line.Green, Line.Red): FareCaps(daily_cap=15, weekly_cap=90),
    (Line.Red, Line.Green): FareCaps(daily_cap=15, weekly_cap=90),
}


# Peak hours
# # # Define peak hours
# | Day       | Start Time | End Time  |
# |-----------|------------|-----------|
# | Monday    | 08:00 AM   | 10:00 AM  |Weekday= 0
# | Monday    | 04:30 PM   | 07:00 PM  |Weekday= 0
# | Tuesday   | 08:00 AM   | 10:00 AM  |Weekday= 1
# | Tuesday   | 04:30 PM   | 07:00 PM  |Weekday= 1
# | Wednesday | 08:00 AM   | 10:00 AM  |Weekday= 2
# | Wednesday | 04:30 PM   | 07:00 PM  |Weekday= 2
# | Thursday  | 08:00 AM   | 10:00 AM  |Weekday= 3
# | Thursday  | 04:30 PM   | 07:00 PM  |Weekday= 3
# | Friday    | 08:00 AM   | 10:00 AM  |Weekday= 4
# | Friday    | 04:30 PM   | 07:00 PM  |Weekday= 4
# | ----------------------------------------------
# | Saturday  | 10:00 AM   | 02:00 PM  |Weekend= 5
# | Saturday  | 06:00 PM   | 11:00 PM  |Weekend= 5
# | Sunday    | 06:00 PM   | 11:00 PM  |Weekend= 6
peak_hours = {
    "Weekday": [(8, 0, 10, 0), (16, 30, 19, 0)],
    "Saturday": [(10, 0, 14, 0), (18, 0, 23, 0)],
    "Sunday": [(18, 0, 23, 0)],
}