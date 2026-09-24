from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import Optional

def get_start_keyboard(last_city: Optional[str] = None) -> ReplyKeyboardMarkup:
    keyboard = []
    
    # Если у пользователя есть сохраненный город, добавляем кнопку для него
    if last_city:
        keyboard.append([KeyboardButton(text=f"Погода в: {last_city}")])
        
    keyboard.append([KeyboardButton(text="Отправить геопозицию", request_location=True)])
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Введите город или отправьте геопозицию..."
    )
