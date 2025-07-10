import unittest
from unittest.mock import patch, mock_open
import json
import sys
import os

# Add the parent directory to sys.path to import the module
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from elections.view import get_elections, get_chosen_election, read_meta_data, is_allowed_to_view, print_election_title, print_votes, print_is_self_voting, print_is_public_election, print_election_creator, print_voters

class TestViewFunctions(unittest.TestCase):

    def setUp(self):
        self.mock_meta_data = {
            "title": "Test Election",
            "creator": "creator@example.com",
            "self_voting": "false",
            "public_election": "true",
            "voters": ["voter1@example.com", "voter2@example.com"],
            "election_data": {"Candidate1": 2, "Candidate2": 3}
        }

    @patch('os.listdir')
    def test_get_elections(self, mock_listdir):
        mock_listdir.return_value = ['election1', 'election2', 'election3']
        with patch('builtins.print') as mock_print:
            result = get_elections()
        self.assertEqual(result, ['election1', 'election2', 'election3'])
        mock_print.assert_any_call('election1')
        mock_print.assert_any_call('election2')
        mock_print.assert_any_call('election3')

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({"key": "value"}))
    def test_read_meta_data(self, mock_file):
        result = read_meta_data("test_election")
        self.assertEqual(result, {"key": "value"})

    @patch('elections.view.read_meta_data')
    def test_is_allowed_to_view(self, mock_read_meta_data):
        mock_read_meta_data.return_value = self.mock_meta_data
        self.assertTrue(is_allowed_to_view("creator@example.com", "test_election"))
        self.assertFalse(is_allowed_to_view("voter1@example.com", "test_election"))
        
        self.mock_meta_data["voters"] = ["everyone"]
        self.assertTrue(is_allowed_to_view("random@example.com", "test_election"))

    @patch('builtins.print')
    def test_print_election_title(self, mock_print):
        print_election_title(self.mock_meta_data)
        mock_print.assert_any_call("The title of this election is: Test Election")

    @patch('builtins.print')
    def test_print_votes(self, mock_print):
        print_votes(self.mock_meta_data)
        mock_print.assert_any_call("2 vote(s) for: Candidate1.")
        mock_print.assert_any_call("3 vote(s) for: Candidate2.")
        mock_print.assert_any_call("Total votes for this election: 5")

    @patch('builtins.print')
    def test_print_is_self_voting(self, mock_print):
        print_is_self_voting(self.mock_meta_data)
        mock_print.assert_any_call("Is the maker of the election allowed to vote?: false")

    @patch('builtins.print')
    def test_print_is_public_election(self, mock_print):
        print_is_public_election(self.mock_meta_data)
        mock_print.assert_any_call("Is this a public election: true")

    @patch('builtins.print')
    def test_print_election_creator(self, mock_print):
        print_election_creator(self.mock_meta_data)
        mock_print.assert_any_call("The creator of this election is: creator@example.com")

    @patch('builtins.print')
    def test_print_voters(self, mock_print):
        print_voters(self.mock_meta_data)
        mock_print.assert_any_call("People allowed to vote in: ['voter1@example.com', 'voter2@example.com']")

if __name__ == '__main__':
    unittest.main()
