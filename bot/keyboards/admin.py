from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Новый пользователь")],
            [KeyboardButton(text="Пользователи")],
            [KeyboardButton(text="Удалить пользователя")],
            [KeyboardButton(text="Помощь")],
        ],
        resize_keyboard=True
    )

def role_selection_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Администратор", callback_data="role_admin")],
            [InlineKeyboardButton(text="Пользователь", callback_data="role_user")],
        ]
    )

def create_user(telegram_id, last_name, first_name, middle_name, email, role):
    with SessionLocal() as session:
        user = User(
            telegram_id=telegram_id,
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            email=email,
            role=role
        )
        session.add(user)
        session.commit()
        return user

def get_all_users():
    with SessionLocal() as session:
        return session.query(User).all()

def delete_user_by_telegram_id(telegram_id):
    with SessionLocal() as session:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            raise ValueError(f"Пользователь с Telegram ID {telegram_id} не найден.")
        session.delete(user)
        session.commit()
        return True

def get_registration_request_by_telegram_id(session, telegram_id):
    # Реализуйте аналогично, если используете модель RegistrationRequest
    pass

def delete_registration_request(session, telegram_id):
    # Реализуйте аналогично, если используете модель RegistrationRequest
    pass