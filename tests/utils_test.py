"""Unit tests for methods in utils.py"""

import unittest
import unittest.mock as mock

import tenk.utils

class UtilsTest(unittest.TestCase):

    @mock.patch('tenk.utils.os.path.exists')
    def test_load_user(self, mock_exists):
        """load_user() should return None if no data exists and create is
        False"""
        mock_exists.return_value = None

        self.assertIsNone(tenk.utils.load_user())

    @mock.patch('builtins.print')
    @mock.patch('tenk.utils.load_user')
    def test_no_user(self, mock_load, mock_print):
        """If no user exists, a message about no data should be printed
        for add_time(), remove_skill(), add_notes()"""
        no_data_msg = "You have no data!"
        mock_load.return_value = False
        tenk.utils.add_time('piano', 1.0)
        mock_print.assert_called_with(no_data_msg)

        tenk.utils.remove_skill('programming')
        mock_print.assert_called_with(no_data_msg)

        tenk.utils.add_notes('programming', {})
        mock_print.assert_called_with(no_data_msg)

if __name__ == '__main__':
    unittest.main()
