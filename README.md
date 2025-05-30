# VARtigrate
Grid Integration Software


## Overview:

VARtigrate is an application for integrating variable availability resources into a mixed source grid, with the ability to optimize the grid's performance and minimize energy waste.  

The system is trained on past weather and energy usage data, as well as a live input of current and predicted weather conditions, which generates an evolving direction of future integration strategies.

## Scope: 

The application will take either real or synthetic energy usage data, coupled with predicted weather data and estimate the renewable energy production.  It will then use this estimate of energy production and an estimate of grid energy needs for a given time in order to optimally distribute the renewable energy.  The app will have ML models that estimate energy production from weather and other factors that would be available in a real-world use case, grid needs based on historical usage information coupled with weather data and things like day of the week and whatever else that is easily obtainable.  This information will be put together to then result in an interface that will describe current grid conditions as well as forecast future grid activity.

## test_eia_collector.py:

| Test Function                               | Method Tested                            | Scenario         | What it Verifies                                   |
| ------------------------------------------- | ---------------------------------------- | ---------------- | -------------------------------------------------- |
| `test_get_electricity_demand`               | `get_electricity_demand()`               | Normal usage     | Parses demand data correctly into a DataFrame      |
| `test_get_renewable_generation`             | `get_renewable_generation()`             | Normal usage     | Handles renewable fuel types and parses generation |
| `test_get_electric_hourly_demand_subregion` | `get_electric_hourly_demand_subregion()` | Normal usage     | Parses subregion demand correctly                  |
| `test_make_request_error_handling`          | `_make_request()`                        | API error occurs | Raises and logs exceptions correctly               |


## Plan:

1. **Data Collection**: 
   - Collect historical weather data and energy usage data.
   - Use APIs to gather real-time weather and energy data.
2. **Data Processing**:
   - Clean and preprocess the data for analysis.
   - Create features that represent weather conditions, energy usage patterns, and other relevant factors.
3. **Model Development**:
    - Develop machine learning models to predict energy production based on weather data
    - Develop models to estimate grid energy needs based on historical usage and weather data 
4. **Integration Strategy**:
   - Create an optimization algorithm to distribute renewable energy based on predictions.
   - Implement a feedback loop to adjust strategies based on real-time data.
5. **User Interface**:
   - Develop a user interface to visualize current grid conditions and future forecasts.
   - Provide insights and recommendations for energy distribution according to the model predictions