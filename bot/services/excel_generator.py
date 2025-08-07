import openpyxl
import shutil
import os

def generate_report(report_data, output_path="data/generated_report.xlsx"):
    template_path = os.path.join('data', 'report_template.xlsx')
    report_path = output_path

    shutil.copy(template_path, report_path)
    wb = openpyxl.load_workbook(report_path)
    ws = wb.active

    # 1. Организация (A6)
    ws['A6'] = report_data.get("employee_organisation", "")

    # 2. ФИО (K22)
    fio = f"{report_data.get('surname', '')} {report_data.get('name', '')} {report_data.get('patronymic_name', '')}".strip()
    ws["K22"] = fio

    # 3. Табельный номер (AR22)
    ws["AR22"] = report_data.get("employee_id", "")

    # 4. Приказ (S67)
    order = report_data.get("order", {})
    if order:  # Проверяем, что order не None
        ws["S67"] = "Приказ"  # <-- только слово "Приказ"
        ws["D67"] = order.get('order_date', '')  # Вставка даты приказа
        ws["J67"] = order.get('order_date', '')  # Вставка даты приказа в J67
        duration = int(order.get("duration", 0) or 0)
    else:
        ws["S67"] = "Приказ не указан"
        ws["D67"] = ""
        ws["J67"] = ""  # Если приказ не указан, ячейка пустая
        duration = 0

    # 5. Срок командировки (S69, AA69)
    ws["S69"] = f"700 * {duration}"
    ws["AA69"] = duration * 700

    # 6. Билеты (D67, J67, AA67 и далее)
    tickets = report_data.get("tickets", [])
    start_row = 67
    for i, ticket in enumerate(tickets):
        row = start_row + i
        ws[f"D{row}"] = ticket.get("ticket_date", "")
        ws[f"J{row}"] = ticket.get("ticket_number", "")
        ws[f"AA{row}"] = float(ticket.get("ticket_price", 0) or 0)

    # 7. Слово "Суточные" (J69)
    ws["J69"] = "Суточные"

    wb.save(report_path)

if __name__ == "__main__":
    # Пример тестовых данных
    report_data = {
        "employee_organisation": "ООО АЛРОСА информационные технологии",
        "surname": "Иванов",
        "name": "Иван",
        "patronymic_name": "Иванович",
        "employee_id": "D8200684",
        "order": {
            "order_number": "123/К",
            "order_date": "01.06.2024",
            "duration": 5
        },
        "tickets": [
            {
                "ticket_date": "02.06.2024",
                "ticket_number": "1234567890",
                "ticket_price": 15000.0
            },
            {
                "ticket_date": "03.06.2024",
                "ticket_number": "0987654321",
                "ticket_price": 12000.0
            }
        ]
    }
    generate_report(report_data)
    print("Отчет сгенерирован и сохранен в data/generated_report.xlsx")