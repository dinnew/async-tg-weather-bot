import aiohttp
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from services.weather_api import get_weather_by_coords, get_locations_by_city
from database.models import UserSetting

router = Router()

async def save_user_location(db_session: AsyncSession, user_id: int, city_name: str, lat: float, lon: float) -> None:
    """Вспомогательная функция для сохранения или обновления города пользователя в БД"""
    try:
        user_setting = UserSetting(
            user_id=user_id,
            city_name=city_name,
            lat=lat,
            lon=lon
        )
        # merge автоматически обновит запись, если user_id существует, или создаст новую
        await db_session.merge(user_setting)
        await db_session.commit()
    except Exception as e:
        # Логируем ошибку, но не ломаем работу бота для пользователя
        import logging
        logging.error(f"Ошибка сохранения в базу данных: {e}")

# 1. Хэндлер на получение координат напрямую с устройства
@router.message(F.location)
async def handle_location_request(message: Message, client_session: aiohttp.ClientSession, db_session: AsyncSession):
    lat = message.location.latitude
    lon = message.location.longitude
    
    await message.answer("Секунду, запрашиваю погоду для вашей локации...")
    
    # Запрашиваем погоду
    report = await get_weather_by_coords(client_session, lat, lon)
    await message.answer(report)
    await save_user_location(db_session, message.from_user.id, "Текущая геопозиция", lat, lon)

# 2. Хэндлер на текстовый ввод города
@router.message(F.text)
async def handle_city_request(message: Message, client_session: aiohttp.ClientSession, db_session: AsyncSession):
    # Если пользователь нажал на кнопку быстрого повтора "Погода в: Город"
    city = message.text.strip()
    if city.startswith("Погода в: "):
        city = city.replace("Погода в: ", "")

    locations = await get_locations_by_city(client_session, city)
                
    if locations is None:
        await message.answer("Произошла ошибка при поиске города.")
        return
        
    if not locations:
        await message.answer("Город не найден. Проверьте правильность написания.")
        return

    # Если найден ровно 1 город
    if len(locations) == 1:
        loc = locations[0]
        lat = loc["lat"]
        lon = loc["lon"]
        name = loc.get("local_names", {}).get("ru", loc["name"])
        
        report = await get_weather_by_coords(client_session, lat, lon)
        await message.answer(report)
        
        # Сохраняем в базу данных
        await save_user_location(db_session, message.from_user.id, name, lat, lon)
        return

    # Если городов несколько — строим inline-клавиатуру
    keyboard_buttons = []
    for loc in locations:
        name = loc.get("local_names", {}).get("ru", loc["name"])
        country = loc["country"]
        state = f", {loc['state']}" if "state" in loc else ""
        
        button_text = f"{name} ({country}{state})"
        # Кодируем в callback_data название города (обрезаем до 20 символов, чтобы влезть в лимит 64 байта)
        # Формат: geo_lat_lon_cityname
        clean_name = name.replace("_", " ")[:20]
        callback_data = f"geo_{loc['lat']:.4f}_{loc['lon']:.4f}_{clean_name}"
        
        keyboard_buttons.append([InlineKeyboardButton(text=button_text, callback_data=callback_data)])
        
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    await message.answer("Найдено несколько мест. Выберите нужное:", reply_markup=reply_markup)

# 3. Обработчик нажатия на inline-кнопки городов
@router.callback_query(F.data.startswith('geo_'))
async def process_city_callback(callback_query: CallbackQuery, client_session: aiohttp.ClientSession, db_session: AsyncSession):
    # Распаковываем данные (теперь там 4 элемента)
    _, lat, lon, city_name = callback_query.data.split('_')
    await callback_query.answer()
    
    lat_float = float(lat)
    lon_float = float(lon)
    
    report = await get_weather_by_coords(client_session, lat_float, lon_float)
    await callback_query.message.edit_text(report)
    
    # Сохраняем выбор пользователя в БД после клика по кнопке
    await save_user_location(db_session, callback_query.from_user.id, city_name, lat_float, lon_float)
