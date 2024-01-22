import asyncio
import datetime
import json
import logging

import python_weather
from python_weather.forecast import HourlyForecast

def get_weather(city: str) -> str:
    return asyncio.run(get_weather_async(city))

async def get_weather_async(city: str = "Vienna") -> str:
    logging.info(f"Gather weather data for city: {city}")
    # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        # fetch a weather forecast from a city
        weather = await client.get(location=city)
        
        # returns the current day's forecast temperature (int)
        #print("Temp: ", weather.current.temperature)
        
        output = {
            "temperature_celsius": weather.current.temperature,
            "wind_speed": weather.current.wind_speed,
            "wind_direction": weather.current.wind_direction.value,
            "humidity": weather.current.humidity
        }

        # get the weather forecast for a few days
        forecast_today = {}
        forecast_tomorrow = {}

        for forecast in weather.forecasts:

            # Forecast today
            if forecast.date == weather.current.date.date():
                for hourly in forecast.hourly:
                    forecast_today[hourly.time.strftime("%H:%M")] = hourly_to_dict(hourly)

            # Forecast tomorrow
            elif forecast.date == weather.current.date.date() + datetime.timedelta(days=1):
                for hourly in forecast.hourly:
                    forecast_tomorrow[hourly.time.strftime("%H:%M")] = hourly_to_dict(hourly)

        output["forecast_today"] = forecast_today
        output["forecast_tomorrow"] = forecast_tomorrow
        
        #hourly forecasts

        return json.dumps(output)
    
def hourly_to_dict(hourly: HourlyForecast):
    return {
        "temperature": hourly.temperature,
        "wind_speed_kmh": hourly.wind_speed,
        "wind_direction": hourly.wind_direction.value,
        "humidity": hourly.humidity,
        "description": hourly.description
    }
        