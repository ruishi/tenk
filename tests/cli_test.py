import unittest
from unittest import mock

from tkcli import main

class CLITest(unittest.TestCase):
    def test_get_note_pairs(self):
        """get_note_pairs should be able to extract note categories and
        contents with regex"""
        # using : as a separator
        note_strs = list()
        note_strs.append(("learned: appregios, chord inversions "
                          "improved : major triad root positions"))
        # using = as a separator
        note_strs.append(("learned = appregios, chord inversions "
                          "improved=major triad root positions"))
        # using both = and : as separators
        note_strs.append(("learned= appregios, chord inversions "
                          "improved:major triad root positions"))
        for note in note_strs:
            note_pairs = main.get_note_pairs(note)
            self.assertEqual(2, len(note_pairs))
            self.assertEqual('learned', note_pairs[0][0])
            self.assertEqual('improved', note_pairs[1][0])
            self.assertEqual('appregios, chord inversions', note_pairs[0][1])
            self.assertEqual('major triad root positions', note_pairs[1][1])

    @mock.patch('builtins.print')
    @mock.patch('tenk.utils.load_user')
    def test_no_user(self, mock_load, mock_print):
        """If no user exists, a message about no data should be printed
        for add_time(), remove_skill(), add_notes()"""
        no_data_msg = "You have no data!"
        mock_load.return_value = False
        main.add_time('piano', 1.0)
        mock_print.assert_called_with(no_data_msg)

        main.remove_skill('programming')
        mock_print.assert_called_with(no_data_msg)

        main.add_notes('programming', {})
        mock_print.assert_called_with(no_data_msg)


if __name__ == '__main__':
    unittest.main()
