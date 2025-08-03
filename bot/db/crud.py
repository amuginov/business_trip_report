from bot.services.database import SessionLocal
from .models import User

def create_user(
    telegram_id,
    surname,
    name,
    patronymic_name,
    email,
    employee_id,
    employee_organisation,
    employee_position,
    role,
    registration_status
):
    with SessionLocal() as session:
        user = User(
            telegram_id=telegram_id,
            surname=surname,
            name=name,
            patronymic_name=patronymic_name,
            email=email,
            employee_id=employee_id,
            employee_organisation=employee_organisation,
            employee_position=employee_position,
            role=role,
            registration_status=registration_status
        )
        session.add(user)
        session.commit()
        return user

def get_all_users():
    with SessionLocal() as session:
        return session.query(User).all()

def get_user_by_telegram_id(telegram_id):
    with SessionLocal() as session:
        return session.query(User).filter(User.telegram_id == telegram_id).first()

def delete_user_by_telegram_id(telegram_id):
    with SessionLocal() as session:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            raise ValueError(f"Пользователь с Telegram ID {telegram_id} не найден.")
        session.delete(user)
        session.commit()
        return True

def get_all_admins():
    with SessionLocal() as session:
        return session.query(User).filter(User.role == "admin").all()

def get_registration_request_by_telegram_id(session, telegram_id):
    return session.query(User).filter(
        User.telegram_id == telegram_id,
        User.registration_status == "pending"
    ).first()

def delete_registration_request(session, telegram_id):
    # Реализуйте аналогично, если используете модель RegistrationRequest
    pass