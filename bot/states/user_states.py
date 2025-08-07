from aiogram.fsm.state import State, StatesGroup

class GuestRegistrationStates(StatesGroup):
    waiting_for_last_name = State()
    waiting_for_first_name = State()
    waiting_for_middle_name = State()
    waiting_for_email = State()
    waiting_for_employee_id = State()
    waiting_for_employee_organisation = State()
    waiting_for_employee_position = State()
    waiting_for_role = State()

class AdminUserCreationStates(StatesGroup):
    waiting_for_last_name = State()
    waiting_for_first_name = State()
    waiting_for_middle_name = State()
    waiting_for_email = State()
    waiting_for_telegram_id = State()
    waiting_for_role = State()

class UserDeletionStates(StatesGroup):
    waiting_for_telegram_id = State()

class AdvanceReportStates(StatesGroup):
    waiting_for_order_pdf = State()
    waiting_for_ticket_pdf = State()
    waiting_for_more_tickets = State()
    waiting_for_manual_ticket_data = State()
    processing = State()