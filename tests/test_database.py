import unittest
from bot.services.database import Database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database()
        self.db.connect()  # Assuming a connect method exists

    def tearDown(self):
        self.db.disconnect()  # Assuming a disconnect method exists

    def test_user_registration(self):
        user_data = {
            'surname': 'Doe',
            'name': 'John',
            'patronymic': 'Smith',
            'email': 'john.doe@example.com',
            'telegram_id': '123456789',
            'role': 'User'
        }
        result = self.db.register_user(user_data)
        self.assertTrue(result)

    def test_get_user(self):
        user_id = 1  # Assuming a user with this ID exists
        user = self.db.get_user(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user['email'], 'john.doe@example.com')

    def test_delete_user(self):
        user_id = 1  # Assuming a user with this ID exists
        result = self.db.delete_user(user_id)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()