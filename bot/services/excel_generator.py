from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

def generate_excel_report(data, template_path, output_path):
    """
    Generates an Excel report based on the provided data and template.

    :param data: Dictionary containing the data to populate the report.
    :param template_path: Path to the Excel template file.
    :param output_path: Path where the generated report will be saved.
    """
    # Load the template workbook
    workbook = load_workbook(template_path)
    sheet = workbook.active

    # Populate the template with data
    for row_index, (key, value) in enumerate(data.items(), start=2):  # Start from row 2 to skip header
        sheet[f'A{row_index}'] = key  # Assuming keys are written in column A
        sheet[f'B{row_index}'] = value  # Assuming values are written in column B

    # Adjust column widths
    for column in sheet.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        sheet.column_dimensions[get_column_letter(column[0].column)].width = adjusted_width

    # Save the generated report
    workbook.save(output_path)