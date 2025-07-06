# FILE: /advance-report-bot/advance-report-bot/bot/utils/constants.py

ROLE_USER = "Авторизованный пользователь"
ROLE_ADMIN = "Администратор"
ROLE_GUEST = "Неавторизованный пользователь"

BUTTON_REGISTER = "Заявка на регистрацию"
BUTTON_HELP = "Помощь"
BUTTON_USERS = "Пользователи"
BUTTON_NEW_USER = "Новый пользователь"
BUTTON_ADVANCE_REPORT = "Авансовый"

MESSAGE_REGISTRATION_REQUEST = "Заявка на регистрацию направлена на рассмотрение администраторам."
MESSAGE_REGISTRATION_APPROVED = "Вы зарегистрированы и можете пользоваться ботом."
MESSAGE_REGISTRATION_DECLINED = "Ваша заявка на регистрацию отклонена."

PDF_ORDER_FIELDS = [
    "Наименование организации",
    "Номер приказа",
    "Дата приказа",
    "Фамилия, имя, отчество",
    "Табельный номер",
    "Структурное подразделение",
    "Должность",
    "Срок командировки (количество дней)"
]

PDF_TICKET_FIELDS = [
    "Дата покупки билета",
    "Номер билета",
    "Стоимость билета"
]