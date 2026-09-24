from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import UserSetting
from keyboards.reply import get_start_keyboard

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message, db_session: AsyncSession) -> None:
    result = await db_session.execute(select(UserSetting).where(UserSetting.user_id == message.from_user.id))
    user_setting = result.scalar_one_or_none()
    
    last_city = user_setting.city_name if user_setting else None

    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}!\n"
        f"Напиши название города или нажми на кнопку ниже.",
        reply_markup=get_start_keyboard(last_city)
    )
