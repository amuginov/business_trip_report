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

def extract_ticket_data(text):
    """
    Функция для извлечения данных из текста билета.
    """
    try:
        data = {}

        # Извлечение данных для 'ticket_date'
        date_match = re.search(
            r'SELLING DATE\s+(\d{2}\.\d{2}\.\d{4})',
            text
        )
        if date_match:
            data['ticket_date'] = date_match.group(1).strip()
            print(f"Извлечено значение 'ticket_date': {data['ticket_date']}")
        else:
            data['ticket_date'] = None
            print("Не удалось извлечь значение 'ticket_date'.")

        # Извлечение данных для 'ticket_number'
        ticket_number_match = re.search(
            r'TICKET NUMBER\s+(\d+)',
            text
        )
        if ticket_number_match:
            data['ticket_number'] = ticket_number_match.group(1).strip()
            print(f"Извлечено значение 'ticket_number': {data['ticket_number']}")
        else:
            data['ticket_number'] = None
            print("Не удалось извлечь значение 'ticket_number'.")

        # Извлечение данных для 'ticket_price'
        # Логика: ищем строку после "Fare Equiv. Taxes Total" и извлекаем цену после последнего RUB
        price_section_match = re.search(
            r'Fare Equiv\. Taxes Total\n(.*)',
            text,
            re.IGNORECASE
        )
        if price_section_match:
            price_section = price_section_match.group(1).strip()
            price_match = re.search(r'RUB.*?(\d{2}\s?\d{3})$', price_section)
            if price_match:
                data['ticket_price'] = price_match.group(1).strip().replace(" ", "")
                print(f"Извлечено значение 'ticket_price': {data['ticket_price']}")
            else:
                data['ticket_price'] = None
                print("Не удалось извлечь значение 'ticket_price'.")
        else:
            data['ticket_price'] = None
            print("Не удалось найти секцию с ценой.")

        return data
    except AttributeError:
        print("Не удалось извлечь все данные. Проверьте формат текста.")
        return None

if __name__ == "__main__":
    # Путь к файлу билета
    file_path = "data/sample_pdfs/e-ticket_continent.pdf"
    
    # Парсинг текста из PDF
    parsed_text = parse_pdf(file_path)
    if parsed_text:
        print("Извлеченный текст:")
        print(parsed_text)
        
        # Извлечение данных билета
        ticket_data = extract_ticket_data(parsed_text)
        if ticket_data:
            print("Извлеченные данные билета:")
            print(ticket_data)
        else:
            print("Не удалось извлечь данные из текста билета.")
    else:
        print("Не удалось извлечь текст из PDF.")