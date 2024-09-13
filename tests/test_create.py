import unittest
from unittest.mock import patch, mock_open
import json
import sys
import os

# Add the parent directory to sys.path to import the module
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from elections.create import create_election, count_directories, get_election_title, get_options_number, get_option, get_data, get_options_details, get_is_self_voting, get_is_public_election, get_voters_number, get_voter_email, get_allowed_voters

class TestCreate(unittest.TestCase):

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('elections.create.count_directories')
    def test_create_election(self, mock_count_directories, mock_json_dump, mock_file, mock_makedirs):
        mock_count_directories.return_value = 0
        title = "Test Election"
        options_and_data = {"Candidate1": "Info1", "Candidate2": "Info2"}
        allow_self_voting = False
        is_public_election = True
        email = "creator@example.com"
        voters_list = ["voter1@example.com", "voter2@example.com"]

        create_election(title, options_and_data, allow_self_voting, is_public_election, email, voters_list)

        mock_makedirs.assert_called_once()
        self.assertEqual(mock_file.call_count, 3)
        self.assertEqual(mock_json_dump.call_count, 2)

    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_count_directories(self, mock_isdir, mock_listdir):
        mock_listdir.return_value = ['dir1', 'file1', 'dir2']
        mock_isdir.side_effect = [True, False, True]
        result = count_directories()
        self.assertEqual(result, 2)

    @patch('builtins.input', return_value='Test Election')
    def test_get_election_title(self, mock_input):
        result = get_election_title()
        self.assertEqual(result, 'Test Election')

    @patch('builtins.input', side_effect=['1', 'a', '2'])
    def test_get_options_number(self, mock_input):
        result = get_options_number()
        self.assertEqual(result, 2)

    @patch('builtins.input', side_effect=['', 'Candidate1'])
    def test_get_option(self, mock_input):
        result = get_option(1)
        self.assertEqual(result, 'Candidate1')

    @patch('builtins.input', return_value='Info1')
    def test_get_data(self, mock_input):
        result = get_data('Candidate1')
        self.assertEqual(result, 'Info1')

    @patch('elections.create.get_option', side_effect=['Candidate1', 'Candidate2'])
    @patch('elections.create.get_data', side_effect=['Info1', 'Info2'])
    def test_get_options_details(self, mock_get_data, mock_get_option):
        result = get_options_details(2)
        expected = {'Candidate1': 'Info1', 'Candidate2': 'Info2'}
        self.assertEqual(result, expected)

    @patch('builtins.input', side_effect=['invalid', 'yes', 'no'])
    def test_get_is_self_voting(self, mock_input):
        result1 = get_is_self_voting()
        self.assertTrue(result1)
        result2 = get_is_self_voting()
        self.assertFalse(result2)

    @patch('builtins.input', side_effect=['invalid', 'yes', 'no'])
    def test_get_is_public_election(self, mock_input):
        result1 = get_is_public_election()
        self.assertTrue(result1)
        result2 = get_is_public_election()
        self.assertFalse(result2)

    @patch('builtins.input', side_effect=['a', '3'])
    def test_get_voters_number(self, mock_input):
        result = get_voters_number()
        self.assertEqual(result, 3)

    @patch('builtins.input', side_effect=['', 'voter@example.com'])
    def test_get_voter_email(self, mock_input):
        result = get_voter_email(1)
        self.assertEqual(result, 'voter@example.com')

    @patch('elections.create.get_voters_number', return_value=2)
    @patch('elections.create.get_voter_email', side_effect=['voter1@example.com', 'voter2@example.com'])
    def test_get_allowed_voters(self, mock_get_voter_email, mock_get_voters_number):
        result_public = get_allowed_voters(True)
        self.assertEqual(result_public, ['everyone'])

        result_private = get_allowed_voters(False)
        self.assertEqual(result_private, ['voter1@example.com', 'voter2@example.com'])

if __name__ == '__main__':
    unittest.main()
