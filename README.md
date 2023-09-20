# Peakflo: Singa Metro Fare Calculator

Singa Metro Authority (SMA) Fare Calculator is a FastAPI-based application for calculating fares for the Singa metro system. It implements fare rules, peak hours, and fare caps for various metro lines.

## Features

- Calculates fares based on the journey's starting and ending lines.
- Considers peak hours for fare calculation.
- Implements daily and weekly fare caps.
- In case the fare meets the cap make the ride free for that day/week
- Allows the user to upload a CSV file with journey data for fare calculation.

## Requirements

- Python 3.8 or later
- FastAPI
- Pydantic
- pytest (for running tests)
- Docker (for containerization)



### Table of Contents

- [Project Setup](#project-overview)
- [Features](#features)
- [Installation Guide](#installation-guide)
- [Usage Guide](#usage-guide)
- [Advanced Usage](#advanced-usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

### Algorithm: Terminologies  

- The action of reducing the fare to make it equal to the daily cap when the sum of the daily fare usage and the current journey's fare  exceeds the daily cap is likely implemented to prevent riders from being charged more than the daily cap for a single day of travel.

Here's a breakdown of why this action is performed:

- Daily Cap Limit: Each day, there is a limit (daily cap) on how much a rider can be charged for their journeys on a specific route or combination of routes. This daily cap is in place to ensure that riders are not financially burdened beyond a certain point in a single day.

- Sum of Daily Fare Usage: The algorithm keeps track of the total fare usage for a specific route or combination of routes in a single day. This sum includes the fares of all journeys taken on that route(s) within the same day.

- Checking Against Daily Cap: When a new journey is added, the algorithm checks if the sum of the daily fare usage and the fare for the current journey exceeds the daily cap.

- Reducing Fare: If this sum is greater than the daily cap, it means the rider would be charged more than the daily cap for that day if the full fare for the current journey is applied. To avoid this, the fare for the current journey is reduced to make it equal to the daily cap. This ensures that the rider is not overcharged for their daily travel on that specific route(s).

In summary, this action is taken to ensure that riders are charged fairly and that they do not exceed the daily cap, which is designed to protect them from excessive charges on any given day.

### Installation Guide

1. **Clone the repository:**

   ```bash
   https://github.com/antrikshdua/Peakflo-Signa-Metro-Fare-Calculator.git
   ```

2. **Setup project locally:**

    ```bash
    python -m venv venv
    ```
    
    ```bash
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
    
3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ````

4. **Run project locally:**

    ```bash
    python main.py
    ```

The server should now be running on `http://localhost:8000`

### Features

- Python 3.8+ support
- Asynchoronous capabilities
- Uvicorn
- Testing suite
- Type checking using pydantic
- Readily available CRUD operations
- Formatting using black

### Usage Guide

The project is designed to be modular and scalable. There are 3 main directories in the project:

1. `core`: This directory contains the central part of this project. It currenty contains cnfig and utils but most of the boiler plate code like security dependencies, database connectionsetc goes here. Overall, the `core` directory is designed to be as generic as possible and can be used in any project.

2. `app`: This directory contains the actual application code. It contains the modules, enums, schemas and business logic. This is the directory you will be spending most of your time in while building features. The directory has following sub-directories:

   - `modules` Here is where you add new modules. this contains teh modules named accordingly with the related version.
   - `v1` Here are the enums, schemad and the business logic corresponding that version of the module. 
   - `schemas` This is where you add the schemas for the application. The schemas are used for validation and serialization/deserialization of the data.
   - `enums` The enums are used for providing the constant values such as schedules, farecaos, fare routes etc.
3. `main.py`: This file contains the API layer of the application and is teh main entry point file. It is where you add the API endpoints.


#### Enums 

The enums are designed based on the tab;le data provided in the problem stattement 

1. **Fare Enum:**

```bash
# Load fare rules and caps from configuration
# Fares
# | FromLine | ToLine | Non-Peak| Peak|
# |----------|--------|----------|-----------|
# | Green    | Green  | 1       | 2        |
# | Red      | Red    | 2       | 3       |
# | Green    | Red    | 3       | 4        |
# | Red      | Green  | 2       | 3        |
```

```python
fare_rules = {
    (Line.Green, Line.Green): FareRules(non_peak=1, peak=2),
    (Line.Red, Line.Red): FareRules(non_peak=2, peak=3),
    (Line.Green, Line.Red): FareRules(non_peak=3, peak=4),
    (Line.Red, Line.Green): FareRules(non_peak=2, peak=3),
}
```

2. **Fare Caps Enum:**

```bash
#Caps
# | FromLine | ToLine | DailyCap | WeeklyCap |
# |-----------|---------|-----------|------------|
# | Green     | Green   | 8         | 55         |
# | Red       | Red     | 12        | 70         |
# | Green     | Red     | 15        | 90         |
# | Red       | Green   | 15        | 90         |
```

```python
fare_caps = {
    (Line.Green, Line.Green): FareCaps(daily_cap=8, weekly_cap=55),
    (Line.Red, Line.Red): FareCaps(daily_cap=12, weekly_cap=70),
    (Line.Green, Line.Red): FareCaps(daily_cap=15, weekly_cap=90),
    (Line.Red, Line.Green): FareCaps(daily_cap=15, weekly_cap=90),
}

```

3. **Peak Hour Schedule Enum:**

```bash
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
```

```python
peak_hours = {
    "Weekday": [(8, 0, 10, 0), (16, 30, 19, 0)],
    "Saturday": [(10, 0, 14, 0), (18, 0, 23, 0)],
    "Sunday": [(18, 0, 23, 0)],
}
```


## Testing

The project contains tests for all endpoints and all the cases, 


#### Test Suite 

```bash
pytest --verbose tests/ 
```

![alt text](https://github.com/antrikshdua/Peakflo-Signa-Metro-Fare-Calculator/blob/main/images/pytest-pass..jpg?raw=true)


#### API Testing

 **Please refer to the screenshot and create a post request accordingly**

#### Test Cases

1. **Normal Route Fare Calculation**

- Add the csv from the test-csv folder named normal-fare-calculation.csv

![alt text](https://github.com/antrikshdua/Peakflo-Signa-Metro-Fare-Calculator/blob/main/images/normal-fare-calculation..jpg?raw=true)



2. **Invalid Route Fare Calculation**

- Add the csv from the test-csv folder named invalid-route-data.csv

![alt text](https://github.com/antrikshdua/Peakflo-Signa-Metro-Fare-Calculator/blob/main/images/normal-fare-calculation..jpg?raw=true)


3. **Daily Limit Exceed**

- Add the csv from the test-csv folder named daily-limit-exceeded.csv

![alt text](https://github.com/antrikshdua/Peakflo-Signa-Metro-Fare-Calculator/blob/main/images/normal-fare-calculation..jpg?raw=true)


4. **Weekly Limit Exceed**

- Add the csv from the test-csv folder named weekly-limit-exceeded.csv

![alt text](https://github.com/antrikshdua/Peakflo-Signa-Metro-Fare-Calculator/blob/main/images/normal-fare-calculation..jpg?raw=true)

## Contributing

Contributions are higly welcome. Please open an issue or a PR if you want to contribute.

## License

<!---
Copyright 2023 The Antriksh Dua team. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->