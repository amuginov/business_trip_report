from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from bot.states.user_states import AdvanceReportStates
from bot.keyboards.user import user_keyboard, more_tickets_keyboard
from bot.services.excel_generator import generate_report
from bot.db.crud import get_user_by_telegram_id  # добавьте импорт
from bot.parsers.order_parser import parse_pdf, extract_order_data  # импорт парсера
from bot.parsers.continent_ticket_parser import parse_pdf as parse_ticket_pdf, extract_ticket_data

router = Router()

@router.message(F.text == "Авансовый")
async def start_advance_report(message: Message, state: FSMContext):
    await message.answer("Вложите pdf-файл с приказом.")
    await state.set_state(AdvanceReportStates.waiting_for_order_pdf)

@router.message(AdvanceReportStates.waiting_for_order_pdf, F.document)
async def get_order_pdf(message: Message, state: FSMContext):
    # Скачайте файл
    file_info = await message.bot.get_file(message.document.file_id)
    file_path = f"data/{message.document.file_name}"
    await message.bot.download_file(file_info.file_path, file_path)
    # Парсим приказ
    text = parse_pdf(file_path)
    order_data = extract_order_data(text) if text else {}
    # Сохраняем результат парсинга в state
    await state.update_data(order=order_data)
    await message.answer("Вложите pdf-файл c билетом.")
    await state.set_state(AdvanceReportStates.waiting_for_ticket_pdf)

@router.message(AdvanceReportStates.waiting_for_ticket_pdf, F.document)
async def get_ticket_pdf(message: Message, state: FSMContext):
    # Скачайте файл билета
    file_info = await message.bot.get_file(message.document.file_id)
    file_path = f"data/{message.document.file_name}"
    await message.bot.download_file(file_info.file_path, file_path)
    # Парсим билет
    text = parse_ticket_pdf(file_path)
    ticket_data = extract_ticket_data(text) if text else {}
    # Добавляем данные билета в список билетов в state
    data = await state.get_data()
    tickets = data.get("tickets", [])
    tickets.append(ticket_data)
    await state.update_data(tickets=tickets)
    await message.answer("Есть ли еще билет?", reply_markup=more_tickets_keyboard())
    await state.set_state(AdvanceReportStates.waiting_for_more_tickets)

@router.callback_query(AdvanceReportStates.waiting_for_more_tickets, F.data == "more_ticket_yes")
async def more_ticket_yes(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Вложите следующий pdf-файл c билетом.")
    await state.set_state(AdvanceReportStates.waiting_for_ticket_pdf)

@router.callback_query(AdvanceReportStates.waiting_for_more_tickets, F.data == "more_ticket_no")
async def more_ticket_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Данные для авансового отчета получены, идет обработка...")
    data = await state.get_data()
    # Получаем пользователя из базы по telegram_id
    user = get_user_by_telegram_id(str(callback.from_user.id))
    report_data = {
        "employee_organisation": user.employee_organisation if user else "",
        "surname": user.surname if user else "",
        "name": user.name if user else "",
        "patronymic_name": user.patronymic_name if user else "",
        "employee_id": user.employee_id if user else "",
        "order": data.get("order", {}),
        "tickets": data.get("tickets", [])
    }
    generate_report(report_data)
    await callback.message.answer_document(FSInputFile("data/generated_report.xlsx"), caption="Ваш авансовый отчет")
    await state.clear()

@router.message(F.text == "Помощь")
async def user_help(message: Message):
    await message.answer(
        "Инструкция по формированию авансового отчета:\n"
        "1. Нажмите 'Авансовый'.\n"
        "2. Загрузите приказ (PDF).\n"
        "3. Загрузите билет(ы) (PDF). После каждого билета отвечайте, есть ли еще билет.\n"
        "4. Дождитесь формирования отчета — он придет вам в чат."
    )