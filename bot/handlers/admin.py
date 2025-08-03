from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.keyboards.admin import admin_keyboard, role_selection_keyboard
from bot.states.user_states import AdminUserCreationStates, UserDeletionStates
from bot.services.user_service import add_user, list_all_users, remove_user
from bot.services.registration_service import approve_registration, reject_registration
from bot.db.crud import get_registration_request_by_telegram_id, delete_registration_request
from bot.services.database import SessionLocal

router = Router()

@router.message(F.text == "Пользователи")
async def list_users(message: Message):
    users = await list_all_users()
    if not users:
        await message.answer("Список пользователей пуст.")
        return
    user_list = "\n".join(
        [f"ID: {user.telegram_id}, ФИО: {user.surname} {user.name} {user.patronymic_name or ''}, Email: {user.email or 'Не указан'}, Роль: {user.role}" for user in users]
    )
    await message.answer(f"Список пользователей:\n\n{user_list}")

@router.message(F.text == "Новый пользователь")
async def start_user_creation(message: Message, state: FSMContext):
    await message.answer("Введите фамилию нового пользователя:")
    await state.set_state(AdminUserCreationStates.waiting_for_last_name)

@router.message(AdminUserCreationStates.waiting_for_last_name)
async def get_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer("Введите имя нового пользователя:")
    await state.set_state(AdminUserCreationStates.waiting_for_first_name)

@router.message(AdminUserCreationStates.waiting_for_first_name)
async def get_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Введите отчество нового пользователя (или напишите 'нет', если отчество отсутствует):")
    await state.set_state(AdminUserCreationStates.waiting_for_middle_name)

@router.message(AdminUserCreationStates.waiting_for_middle_name)
async def get_middle_name(message: Message, state: FSMContext):
    middle_name = message.text if message.text.lower() != "нет" else None
    await state.update_data(middle_name=middle_name)
    await message.answer("Введите email нового пользователя:")
    await state.set_state(AdminUserCreationStates.waiting_for_email)

@router.message(AdminUserCreationStates.waiting_for_email)
async def get_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введите Telegram ID нового пользователя:")
    await state.set_state(AdminUserCreationStates.waiting_for_telegram_id)

@router.message(AdminUserCreationStates.waiting_for_telegram_id)
async def get_telegram_id(message: Message, state: FSMContext):
    try:
        telegram_id = int(message.text)
        await state.update_data(telegram_id=telegram_id)
        await message.answer("Выберите роль пользователя:", reply_markup=role_selection_keyboard())
        await state.set_state(AdminUserCreationStates.waiting_for_role)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный Telegram ID (число).")

@router.callback_query(AdminUserCreationStates.waiting_for_role)
async def get_role(callback_query: CallbackQuery, state: FSMContext):
    role_mapping = {
        "role_admin": "admin",
        "role_user": "user"
    }
    role = role_mapping.get(callback_query.data)
    if not role:
        await callback_query.message.answer("Пожалуйста, выберите роль из предложенных вариантов.")
        return
    user_data = await state.get_data()
    await add_user(
        telegram_id=user_data["telegram_id"],
        last_name=user_data["last_name"],
        first_name=user_data["first_name"],
        middle_name=user_data["middle_name"],
        email=user_data["email"],
        role=role
    )
    await callback_query.message.answer("Пользователь успешно добавлен!")
    await state.clear()

@router.message(F.text == "Удалить пользователя")
async def start_user_deletion(message: Message, state: FSMContext):
    await message.answer("Введите Telegram ID пользователя, которого вы хотите удалить:")
    await state.set_state(UserDeletionStates.waiting_for_telegram_id)

@router.message(UserDeletionStates.waiting_for_telegram_id)
async def delete_user(message: Message, state: FSMContext):
    try:
        telegram_id = int(message.text)
        await remove_user(telegram_id)
        await message.answer(f"Пользователь с Telegram ID {telegram_id} успешно удален!")
        await state.clear()
    except ValueError as e:
        await message.answer(str(e))
        await state.clear()
    except Exception as e:
        await message.answer(f"Произошла ошибка при удалении пользователя: {e}")
        await state.clear()

@router.callback_query(F.data.startswith("approve:"))
async def approve_user(callback_query: CallbackQuery):
    telegram_id = callback_query.data.split(":")[1]
    with SessionLocal() as session:
        user = get_registration_request_by_telegram_id(session, telegram_id)
        if not user:
            await callback_query.message.answer("Ошибка: Заявка на регистрацию не найдена.")
            return
        try:
            user.role = "authorized"
            user.registration_status = "approved"
            session.commit()
            await callback_query.message.answer(
                f"Пользователь {user.surname} {user.name} ({user.employee_id}, {user.employee_organisation}, {user.employee_position}) успешно зарегистрирован."
            )
        except Exception as e:
            await callback_query.message.answer(f"Произошла ошибка при регистрации пользователя: {e}")

@router.callback_query(F.data.startswith("reject:"))
async def reject_user(callback_query: CallbackQuery):
    telegram_id = callback_query.data.split(":")[1]
    with SessionLocal() as session:
        user = get_registration_request_by_telegram_id(session, telegram_id)
        if not user:
            await callback_query.message.answer("Ошибка: Заявка на регистрацию не найдена.")
            return
        try:
            user.registration_status = "rejected"
            session.commit()
            await callback_query.message.answer(
                f"Заявка пользователя {user.surname} {user.name} отклонена."
            )
        except Exception as e:
            await callback_query.message.answer(f"Произошла ошибка при отклонении заявки: {e}")

@router.message(F.text == "Помощь")
async def admin_help(message: Message):
    await message.answer(
        "Доступные действия администратора:\n"
        "- Новый пользователь: добавить пользователя\n"
        "- Пользователи: список всех пользователей\n"
        "- Удалить пользователя: удалить пользователя по Telegram ID\n"
        "- Помощь: показать это сообщение"
    )