import logging
from typing import Optional, List, Dict, Any
import aiohttp
from aiogram import html
from config import config

WEATHER_API_KEY = config.openweathermap_key.get_secret_value()

async def get_weather_by_coords(session: aiohttp.ClientSession, lat: float, lon: float) -> str:
    weather_url = f"https://openweathermap.org{lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    try:
        async with session.get(weather_url) as response:
            if response.status != 200:
                return "Не удалось получить данные о погоде (Ошибка API)."
            
            data = await response.json()
            city_name = data["name"]
            temp = round(data["main"]["temp"])
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"].capitalize()
            country = data["sys"]["country"]
            
            return (
                f"Погода в: {html.bold(city_name)} ({country})\n"
                f"Температура: {temp}°C\n"
                f"Влажность: {humidity}%\n"
                f"Состояние: {description}"
            )
    except Exception as e:
        logging.error(f"Ошибка при запросе погоды: {e}")
        return "Произошла ошибка при получении данных о погоде."

async def get_locations_by_city(session: aiohttp.ClientSession, city: str) -> Optional[List[Dict[str, Any]]]:
    geo_url = f"https://openweathermap.org{city}&limit=5&appid={WEATHER_API_KEY}"
    try:
        async with session.get(geo_url) as response:
            if response.status != 200:
                return None
            return await response.json()
    except Exception as e:
        logging.error(f"Ошибка поиска города: {e}")
        return None
