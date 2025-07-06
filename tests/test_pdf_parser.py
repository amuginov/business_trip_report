import unittest
from bot.services.pdf_parser import parse_order_pdf, parse_ticket_pdf

class TestPDFParser(unittest.TestCase):

    def test_parse_order_pdf(self):
        # Test parsing of a sample order PDF
        result = parse_order_pdf('data/sample_pdfs/sample_order.pdf')
        expected = {
            'organization_name': 'Sample Organization',
            'order_number': '12345',
            'order_date': '2023-01-01',
            'full_name': 'Иванов Иван Иванович',
            'employee_id': '123456',
            'department': 'Отдел продаж',
            'position': 'Менеджер',
            'trip_duration': 5
        }
        self.assertEqual(result, expected)

    def test_parse_ticket_pdf_s7(self):
        # Test parsing of a sample S7 ticket PDF
        result = parse_ticket_pdf('data/sample_pdfs/sample_ticket_s7.pdf')
        expected = {
            'purchase_date': '2023-01-02',
            'ticket_number': 'S7-987654',
            'ticket_price': 15000
        }
        self.assertEqual(result, expected)

    def test_parse_ticket_pdf_alrosa(self):
        # Test parsing of a sample ALROSA ticket PDF
        result = parse_ticket_pdf('data/sample_pdfs/sample_ticket_alrosa.pdf')
        expected = {
            'purchase_date': '2023-01-03',
            'ticket_number': 'ALR-123456',
            'ticket_price': 12000
        }
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()