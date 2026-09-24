# Async Telegram Weather Bot

A production-ready asynchronous Telegram bot that provides real-time weather information using the OpenWeatherMap API. Built with modern Python tools and clean architecture.

## Features

- **Asynchronous Architecture:** Powered by `aiogram 3.x` and `aiohttp` for high performance.
- **Smart Geocoding:** Automatically handles multiple cities with the same name via interactive inline keyboards.
- **Location Support:** Users can share their GPS location via a mobile device to fetch instantaneous forecasts.
- **Persistent Storage:** Uses `SQLAlchemy 2.0` (Async ORM) and `SQLite` to remember the user's last searched location.
- **Safe Configurations:** Environment variables validation using `Pydantic-settings`.
- **Dockerized:** Fully containerized for easy and fast deployment.

## Tech Stack

- **Language:** Python 3.11+
- **Framework:** Aiogram 3.x (Async Telegram Bots framework)
- **HTTP Client:** Aiohttp (Asynchronous requests)
- **Database / ORM:** SQLite + SQLAlchemy 2.0 (Async Engine)
- **Settings Management:** Pydantic & Python-dotenv
- **DevOps:** Docker & Docker Compose

## Installation & Setup

### Option 1: Using Docker (Recommended)

1. Clone this repository:
   ```bash
   git clone https://github.com
   cd weather-bot
   ```

2. Create a `.env` file in the root directory and add your secret tokens:
   ```env
   TELEGRAM_TOKEN=your_telegram_bot_token_here
   OPENWEATHERMAP_KEY=your_openweathermap_api_key_here
   ```

3. Run the application using Docker Compose:
   ```bash
   docker compose up -d --build
   ```

### Option 2: Local Run

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure your `.env` file as shown above.
3. Start the bot:
   ```bash
   python main.py
   ```

## Project Structure

```text
weather_bot/
├── database/         # Async database layer (SQLAlchemy models & sessions)
├── handlers/         # UI event logic (commands, text inputs, callbacks)
├── keyboards/        # Reply and Inline keyboards layouts
├── services/         # Third-party OpenWeather API connections
├── config.py         # Environment configurations validator
└── main.py           # Application entry point & orchestration
```

## Database Schema

The project uses SQLite with SQLAlchemy Async Engine. The database consists of a single table `user_settings` to persist user preferences:

| Column Name | Data Type | Properties | Description |
| :--- | :--- | :--- | :--- |
| `user_id` | BigInteger | Primary Key | Unique Telegram User ID |
| `city_name` | String(100) | Not Null | Name of the last searched city |
| `lat` | Float | Not Null | Latitude coordinate of the city |
| `lon` | Float | Not Null | Longitude coordinate of the city |
