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

        # Извлечение данных для 'ticket_price' - ОПТИМИЗИРОВАННЫЙ ПАРСЕР
        # Множественные паттерны в порядке приоритета для максимальной точности
        price_patterns = [
            # Специальный паттерн для e-ticket_continent - число в конце строки после YQ
            (0, r'YQ.*?(\d{2}\s\d{3})(?:\s*$|\s*\n)'),
            
            # Основной паттерн - цена в конце строки после YQ с RUB
            (1, r'(?:YQ.*?)?(\d{2}[\s,]?\d{3})\s*RUB(?:\s*$|\s*[\n;])'),
            
            # Цена в формате XX XXX RUB в конце строки
            (2, r'(\d{2}[\s,]?\d{3})\s*RUB\s*$'),
            
            # Цена после множественных RUB
            (3, r'RUB.*?(\d{2}[\s,]?\d{3})\s*RUB'),
            
            # Универсальный - любая большая цена с RUB
            (4, r'(?:^|\s)(\d{2}[\s,]?\d{3})\s*RUB(?:\s|$)'),
            
            # Оригинальный паттерн для совместимости
            (5, r'RUB.*?(\d{2}\s?\d{3})$')
        ]
        
        all_prices = []
        
        # Пробуем все паттерны и собираем результаты
        for priority, pattern in price_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            
            for match in matches:
                cleaned = re.sub(r'[^\d]', '', str(match))
                if cleaned and len(cleaned) >= 4:  # Минимум 4 цифры
                    all_prices.append({
                        'priority': priority,
                        'cleaned': cleaned,
                        'value': int(cleaned)
                    })
        
        if all_prices:
            # Группируем по ценам
            price_groups = {}
            for price_info in all_prices:
                price = price_info['cleaned']
                if price not in price_groups:
                    price_groups[price] = []
                price_groups[price].append(price_info)
            
            # Выбираем лучшую цену по приоритету, при равном приоритете - большую
            best_price = None
            best_priority = float('inf')
            
            for price, infos in price_groups.items():
                min_priority = min(info['priority'] for info in infos)
                price_value = int(price)
                
                if (min_priority < best_priority or 
                    (min_priority == best_priority and price_value > int(best_price or '0'))):
                    best_price = price
                    best_priority = min_priority
            
            if best_price:
                data['ticket_price'] = best_price
                print(f"Извлечено значение 'ticket_price': {data['ticket_price']} (приоритет: {best_priority})")
            else:
                data['ticket_price'] = None
                print("Не удалось выбрать оптимальную цену.")
        else:
            data['ticket_price'] = None
            print("Не удалось извлечь значение 'ticket_price'.")

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