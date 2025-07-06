import unittest
from bot.services.excel_generator import generate_excel_report

class TestExcelGenerator(unittest.TestCase):

    def setUp(self):
        # Setup code to initialize any required resources before each test
        self.sample_data = {
            'organization': 'Test Org',
            'order_number': '12345',
            'date': '2023-10-01',
            'full_name': 'Иванов Иван Иванович',
            'employee_id': '001',
            'department': 'IT',
            'position': 'Developer',
            'trip_duration': 5,
            'tickets': [
                {'date': '2023-10-01', 'ticket_number': 'T123', 'price': 1000},
                {'date': '2023-10-02', 'ticket_number': 'T124', 'price': 1500}
            ]
        }

    def test_generate_excel_report(self):
        # Test the generation of the Excel report
        report_file = generate_excel_report(self.sample_data)
        self.assertTrue(report_file.endswith('.xlsx'))

    def tearDown(self):
        # Cleanup code to remove any resources after each test
        pass

if __name__ == '__main__':
    unittest.main()