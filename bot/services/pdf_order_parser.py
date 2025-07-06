import pdfplumber
import re

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

        # Остальные данные (пока не изменяем)
        data['employee_name'] = re.search(r'Мугинова Азата Рустамовича', text).group(1).strip()
        data['employee_id'] = re.search(r'Табельный номер\s*([A-Za-z0-9]+)', text).group(1).strip()
        data['position'] = re.search(r'должность\s*(.+)', text, re.IGNORECASE).group(1).strip()
        data['duration'] = re.search(r'сроком на\s*(\d+)\s*календарных дней', text).group(1).strip()
        return data
    except AttributeError:
        print("Не удалось извлечь все данные. Проверьте формат текста.")
        return None

if __name__ == "__main__":
    # Путь к файлу приказа
    file_path = "/Users/azatmuginov/business_trip_report/data/sample_pdfs/order.pdf"
    
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