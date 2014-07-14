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
        config = {'PATHS': {'tk_dir': '/nonexistent_dir'}}
        self.assertIsNone(tenk.utils.load_user(config=config))

if __name__ == '__main__':
    unittest.main()
