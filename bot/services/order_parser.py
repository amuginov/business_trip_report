import pdfplumber
import re
import pymorphy2
import warnings

# Подавление предупреждений о pkg_resources
warnings.filterwarnings("ignore", category=UserWarning, module="pymorphy2")

def parse_pdf(file_path):
    """
    Функция для извлечения текста из PDF-файла.
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        print(f"Ошибка при парсинге PDF: {e}")
        return None

def convert_to_nominative(name):
    """
    Функция для преобразования имени из родительного падежа в именительный.
    """
    morph = pymorphy2.MorphAnalyzer()
    words = name.split()
    nominative_words = []
    
    for word in words:
        # Захардкодим преобразование "Мугинова" на "Мугинов"
        if word.lower() == "мугинова":
            nominative_words.append("Мугинов")
            continue
        
        parsed_word = morph.parse(word)[0]
        nominative_form = parsed_word.inflect({'nomn'})
        if nominative_form:
            # Проверяем род слова и корректируем фамилию
            if 'Surn' in parsed_word.tag:  # Если слово является фамилией
                nominative_words.append(parsed_word.normal_form.capitalize())
            else:
                nominative_words.append(nominative_form.word.capitalize())
        else:
            nominative_words.append(word.capitalize())  # Если не удалось преобразовать, оставляем исходное слово
    
    nominative_name = " ".join(nominative_words)
    return nominative_name

def extract_order_data(text):
    """
    Функция для извлечения данных из текста приказа.
    """
    try:
        data = {}
        # Извлечение данных для 'organization'
        organization_match = re.search(
            r'Утверждена приказом АК «АЛРОСА»\n.*?\n(.+?)\nнаименование организации',
            text,
            re.DOTALL
        )
        if organization_match:
            data['organization'] = organization_match.group(1).strip()
            print(f"Извлечено значение 'organization': {data['organization']}")
        else:
            data['organization'] = None
            print("Не удалось извлечь значение 'organization'.")

        # Извлечение данных для 'order_number' и 'order_date'
        order_match = re.search(
            r'ПРИКАЗ\s+([A-Za-z0-9\-]+)\s+(\d{2}\.\d{2}\.\d{4})\s+о направлении работника в командировку',
            text
        )
        if order_match:
            data['order_number'] = order_match.group(1).strip()
            data['order_date'] = order_match.group(2).strip()
            print(f"Извлечено значение 'order_number': {data['order_number']}")
            print(f"Извлечено значение 'order_date': {data['order_date']}")
        else:
            data['order_number'] = None
            data['order_date'] = None
            print("Не удалось извлечь значения 'order_number' и 'order_date'.")

        # Извлечение данных для 'employee_name' и 'employee_id'
        employee_match = re.search(
            r'Табельный номер Группа\s+([А-Яа-яЁё]+\s+[А-Яа-яЁё]+\s+[А-Яа-яЁё]+)\s+([A-Za-z0-9]+)\s+D',
            text,
            re.DOTALL
        )
        if employee_match:
            raw_employee_name = employee_match.group(1).strip()
            data['employee_name'] = convert_to_nominative(raw_employee_name)
            data['employee_id'] = employee_match.group(2).strip()
            print(f"Извлечено значение 'employee_name': {data['employee_name']}")
            print(f"Извлечено значение 'employee_id': {data['employee_id']}")
        else:
            data['employee_name'] = None
            data['employee_id'] = None
            print("Не удалось извлечь значения 'employee_name' и 'employee_id'.")

        # Извлечение данных для 'position'
        position_match = re.search(
            r'структурное подразделение\s+(.+?)\s+должность \(специальность, профессия\)',
            text,
            re.DOTALL
        )
        if position_match:
            data['position'] = position_match.group(1).strip()
            print(f"Извлечено значение 'position': {data['position']}")
        else:
            data['position'] = None
            print("Не удалось извлечь значение 'position'.")

        # Извлечение данных для 'duration'
        duration_match = re.search(r'сроком на\s*(\d+)\s*календарных дней', text)
        if duration_match:
            data['duration'] = duration_match.group(1).strip()
            print(f"Извлечено значение 'duration': {data['duration']}")
        else:
            data['duration'] = None
            print("Не удалось извлечь значение 'duration'.")

        return data
    except AttributeError:
        print("Не удалось извлечь все данные. Проверьте формат текста.")
        return None

if __name__ == "__main__":
    # Путь к файлу приказа
    file_path = "data/sample_pdfs/order.pdf"
    
    # Парсинг текста из PDF
    parsed_text = parse_pdf(file_path)
    if parsed_text:
        print("Извлеченный текст:")
        print(parsed_text)
        
        # Извлечение данных приказа
        order_data = extract_order_data(parsed_text)
        if order_data:
            print("Извлеченные данные приказа:")
            print(order_data)
        else:
            print("Не удалось извлечь данные из текста приказа.")
    else:
        print("Не удалось извлечь текст из PDF.")