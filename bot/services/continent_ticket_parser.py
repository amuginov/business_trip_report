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

if __name__ == "__main__":
    # Путь к файлу билета s7
    file_path = "data/sample_pdfs/e-ticket_continent.pdf"
    
    # Парсинг текста из PDF
    parsed_text = parse_pdf(file_path)
    if parsed_text:
        print("Извлеченный текст:")
        print(parsed_text)
    else:
        print("Не удалось извлечь текст из PDF.")
        