import openpyxl
import shutil
import os

def generate_report(output_path):
    # Пути к шаблону и новому файлу
    template_path = os.path.join('data', 'report_template.xlsx')
    report_path = output_path

    # Копируем шаблон, чтобы не портить оригинал
    shutil.copy(template_path, report_path)

    # Открываем скопированный файл
    wb = openpyxl.load_workbook(report_path)
    ws = wb.active

    # Вставляем текст в ячейку A6
    ws['A6'] = 'ООО "АЛРОСА Информационные технологии"'

    # Сохраняем изменения
    wb.save(report_path)

if __name__ == "__main__":
    generate_report('data/generated_report.xlsx')
    print("Отчет сгенерирован и сохранен в data/generated_report.xlsx")