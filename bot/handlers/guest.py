from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.keyboards.guest_keyboard import guest_keyboard
from bot.states.user_states import GuestRegistrationStates

router = Router()

@router.message(F.text == "Помощь")
async def guest_help(message: Message):
    await message.answer(
        "Бот предназначен для автоматизации авансовых отчетов командировки.\n\nВы можете:\n- Оформить заявку на регистрацию\n- Получить справку по работе с ботом"
    )

@router.message(F.text == "Заявка на регистрацию")
async def guest_registration(message: Message, state: FSMContext):
    await message.answer("Введите вашу фамилию:")
    await state.set_state(GuestRegistrationStates.waiting_for_last_name)

@router.message(GuestRegistrationStates.waiting_for_last_name)
async def get_last_name(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer("Введите ваше имя:")
    await state.set_state(GuestRegistrationStates.waiting_for_first_name)

@router.message(GuestRegistrationStates.waiting_for_first_name)
async def get_first_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваше отчество (или напишите 'нет', если отчество отсутствует):")
    await state.set_state(GuestRegistrationStates.waiting_for_middle_name)

@router.message(GuestRegistrationStates.waiting_for_middle_name)
async def get_middle_name(message: Message, state: FSMContext):
    patronymic_name = message.text if message.text.lower() != "нет" else None
    await state.update_data(patronymic_name=patronymic_name)
    await message.answer("Введите ваш email:")
    await state.set_state(GuestRegistrationStates.waiting_for_email)

@router.message(GuestRegistrationStates.waiting_for_email)
async def get_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введите ваш табельный номер:")
    await state.set_state(GuestRegistrationStates.waiting_for_employee_id)

@router.message(GuestRegistrationStates.waiting_for_employee_id)
async def get_employee_id(message: Message, state: FSMContext):
    await state.update_data(employee_id=message.text)
    await message.answer("Введите вашу организацию:")
    await state.set_state(GuestRegistrationStates.waiting_for_employee_organisation)

@router.message(GuestRegistrationStates.waiting_for_employee_organisation)
async def get_employee_organisation(message: Message, state: FSMContext):
    await state.update_data(employee_organisation=message.text)
    await message.answer("Введите вашу должность:")
    await state.set_state(GuestRegistrationStates.waiting_for_employee_position)

@router.message(GuestRegistrationStates.waiting_for_employee_position)
async def get_employee_position(message: Message, state: FSMContext):
    await state.update_data(employee_position=message.text)
    # Сохраняем заявку и уведомляем админов
    data = await state.get_data()
    data["telegram_id"] = str(message.from_user.id)
    data["role"] = "unauthorized"
    data["registration_status"] = "pending"
    # Здесь вызовите функцию сохранения заявки и уведомления админов
    from bot.services.registration_service import create_registration_request_and_notify_admins
    await create_registration_request_and_notify_admins(data, message)
    await message.answer("Ваша заявка на регистрацию отправлена! Ожидайте подтверждения от администратора.")
    await state.clear()