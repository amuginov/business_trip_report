from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def user_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Авансовый")],
            [KeyboardButton(text="Помощь")]
        ],
        resize_keyboard=True
    )

def more_tickets_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да", callback_data="more_ticket_yes"),
                InlineKeyboardButton(text="Нет", callback_data="more_ticket_no"),
            ]
        ]
    )