from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.states.user_states import GuestRegistrationStates
from bot.keyboards.admin import admin_keyboard
from bot.keyboards.guest_keyboard import guest_keyboard
from bot.keyboards.user import user_keyboard
from bot.db.crud import get_user_by_telegram_id

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message):
    user = get_user_by_telegram_id(str(message.from_user.id))
    if user:
        if user.role == "admin":
            await message.answer(
                "Добро пожаловать, администратор!\n\nДоступные действия:",
                reply_markup=admin_keyboard()
            )
        elif user.role == "authorized":
            await message.answer(
                "Добро пожаловать!\n\nВы авторизованы. Доступные действия:",
                reply_markup=user_keyboard()
            )
        else:
            await message.answer(
                "Добро пожаловать!\n\nВы не авторизованы. Доступные действия:",
                reply_markup=guest_keyboard()
            )
    else:
        await message.answer(
            "Добро пожаловать!\n\nВы не авторизованы. Доступные действия:",
            reply_markup=guest_keyboard()
        )

# Если нужны гостевые хендлеры — реализуйте их здесь или оставьте только в guest.py