import unittest
from bot.handlers.admin_handlers import handle_admin_command
from bot.handlers.user_handlers import handle_user_command
from bot.handlers.guest_handlers import handle_guest_command

class TestHandlers(unittest.TestCase):

    def test_handle_admin_command(self):
        # Test admin command handling
        response = handle_admin_command('some_admin_command')
        self.assertEqual(response, 'Expected response for admin command')

    def test_handle_user_command(self):
        # Test user command handling
        response = handle_user_command('some_user_command')
        self.assertEqual(response, 'Expected response for user command')

    def test_handle_guest_command(self):
        # Test guest command handling
        response = handle_guest_command('some_guest_command')
        self.assertEqual(response, 'Expected response for guest command')

if __name__ == '__main__':
    unittest.main()