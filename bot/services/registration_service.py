from bot.db.crud import create_user, delete_user_by_telegram_id, get_user_by_telegram_id, get_all_admins
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot

async def approve_registration(user_data):
    """
    Регистрирует пользователя.
    """
    try:
        # Проверяем, существует ли пользователь с таким Telegram ID
        existing_user = get_user_by_telegram_id(user_data["telegram_id"])
        if existing_user:
            raise ValueError(f"Пользователь с Telegram ID {user_data['telegram_id']} уже существует.")

        create_user(
            telegram_id=user_data["telegram_id"],
            last_name=user_data["last_name"],
            first_name=user_data["first_name"],
            middle_name=user_data["middle_name"],
            email=user_data["email"],
            role=user_data["role"]
        )
    except Exception as e:
        raise Exception(f"Ошибка при регистрации пользователя: {e}")

async def reject_registration(telegram_id):
    """
    Отклоняет заявку на регистрацию.
    """
    try:
        delete_user_by_telegram_id(telegram_id)
    except Exception as e:
        raise Exception(f"Ошибка при отклонении заявки: {e}")

async def create_registration_request_and_notify_admins(user_data, message: Message):
    # Сохраняем заявку (пользователь с ролью unauthorized и статусом pending)
    create_user(
        telegram_id=user_data["telegram_id"],
        surname=user_data["surname"],
        name=user_data["name"],
        patronymic_name=user_data["patronymic_name"],
        email=user_data["email"],
        employee_id=user_data["employee_id"],
        employee_organisation=user_data["employee_organisation"],
        employee_position=user_data["employee_position"],
        role="unauthorized",
        registration_status="pending"
    )
    # Уведомляем всех админов
    admins = get_all_admins()
    approve_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Одобрить", callback_data=f"approve:{user_data['telegram_id']}"),
                InlineKeyboardButton(text="Отклонить", callback_data=f"reject:{user_data['telegram_id']}")
            ]
        ]
    )
    text = (
        f"Новая заявка на регистрацию:\n"
        f"Фамилия: {user_data['surname']}\n"
        f"Имя: {user_data['name']}\n"
        f"Отчество: {user_data['patronymic_name'] or 'нет'}\n"
        f"Email: {user_data['email']}\n"
        f"Табельный номер: {user_data['employee_id']}\n"
        f"Организация: {user_data['employee_organisation']}\n"
        f"Должность: {user_data['employee_position']}\n"
        f"Telegram ID: {user_data['telegram_id']}"
    )
    bot: Bot = message.bot
    for admin in admins:
        await bot.send_message(admin.telegram_id, text, reply_markup=approve_markup)