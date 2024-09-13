import unittest
from unittest.mock import patch, mock_open
import json
import sys
import os

# Add the parent directory to sys.path to import the module
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from elections.participate import is_allowed_to_vote, read_vote_data, read_candidate_data, get_candidates, prompt_for_option, write_vote, get_secret_email, update_vote_score

class TestParticipate(unittest.TestCase):

    def setUp(self):
        self.mock_meta_data = {
            "creator": "creator@example.com",
            "self_voting": "false",
            "voters": ["voter1@example.com", "voter2@example.com"],
            "election_data": {"Candidate1": 0, "Candidate2": 0}
        }

    @patch('elections.participate.view.read_meta_data')
    @patch('elections.participate.read_vote_data')
    def test_is_allowed_to_vote(self, mock_read_vote_data, mock_read_meta_data):
        mock_read_meta_data.return_value = self.mock_meta_data
        mock_read_vote_data.return_value = []

        self.assertTrue(is_allowed_to_vote("voter1@example.com", "test_election"))
        self.assertFalse(is_allowed_to_vote("creator@example.com", "test_election"))
        self.assertFalse(is_allowed_to_vote("unauthorized@example.com", "test_election"))

    @patch('builtins.open', new_callable=mock_open, read_data=b'encrypted_email1\nencrypted_email2\n')
    @patch('elections.participate.encryption.decrypt_email')
    def test_read_vote_data(self, mock_decrypt_email, mock_file):
        mock_decrypt_email.side_effect = ["voter1@example.com", "voter2@example.com"]
        result = read_vote_data("test_election")
        self.assertEqual(result, ["voter1@example.com", "voter2@example.com"])

    @patch('builtins.open', new_callable=mock_open, read_data='{"Candidate1": "Info1", "Candidate2": "Info2"}')
    def test_read_candidate_data(self, mock_file):
        result = read_candidate_data("test_election")
        self.assertEqual(result, {"Candidate1": "Info1", "Candidate2": "Info2"})

    @patch('elections.participate.read_candidate_data')
    def test_get_candidates(self, mock_read_candidate_data):
        mock_read_candidate_data.return_value = {"Candidate1": "Info1", "Candidate2": "Info2"}
        result = get_candidates("test_election")
        self.assertEqual(result, [["Candidate1", "Info1"], ["Candidate2", "Info2"]])

    @patch('builtins.input', side_effect=['3', '0', 'a', '2'])
    def test_prompt_for_option(self, mock_input):
        candidate_list = [["Candidate1", "Info1"], ["Candidate2", "Info2"]]
        result = prompt_for_option(candidate_list)
        self.assertEqual(result, 2)

    @patch('builtins.open', new_callable=mock_open)
    @patch('elections.participate.encryption.encrypt_email')
    def test_write_vote(self, mock_encrypt_email, mock_file):
        mock_encrypt_email.return_value = b'encrypted_email'
        write_vote("test_election", "voter@example.com", "Candidate1")
        mock_file().write.assert_called_once_with(b'encrypted_email\n')

    @patch('elections.participate.encryption.encrypt_email')
    def test_get_secret_email(self, mock_encrypt_email):
        mock_encrypt_email.return_value = b'encrypted_email'
        result = get_secret_email("voter@example.com")
        self.assertEqual(result, b'encrypted_email')

    @patch('elections.participate.view.read_meta_data')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_update_vote_score(self, mock_json_dump, mock_file, mock_read_meta_data):
        mock_read_meta_data.return_value = self.mock_meta_data
        update_vote_score("test_election", "Candidate1")
        self.assertEqual(self.mock_meta_data["election_data"]["Candidate1"], 1)
        mock_json_dump.assert_called_once()

if __name__ == '__main__':
    unittest.main()
