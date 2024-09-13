import unittest
from io import StringIO
import sys
import io
from unittest.mock import patch
import os

# Add the parent directory to sys.path to import the module
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import project

class TestVotingApp(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('builtins.input')
        self.mock_input = self.patcher.start()
        self.mock_stdout = StringIO()
        sys.stdout = self.mock_stdout

    def tearDown(self):
        self.patcher.stop()
        sys.stdout = sys.__stdout__

    def test_start_app_login(self):
        self.mock_input.side_effect = ["1"]
        with patch('project.authentication.authenticate') as mock_auth:
            with patch('project.authentication.get_user_data') as mock_get_user:
                mock_auth.return_value = "mock_creds"
                mock_get_user.return_value = "user@example.com"
                project.start_app()
        self.assertIn("Trying to log in...", self.mock_stdout.getvalue())

    def test_start_app_exit(self):
        self.mock_input.side_effect = ["2"]
        with self.assertRaises(SystemExit):
            project.start_app()
        self.assertIn("Logging out...", self.mock_stdout.getvalue())

    def test_start_app_invalid_input(self):
        self.mock_input.side_effect = ["3", "2"]
        with self.assertRaises(SystemExit):
            project.start_app()
        self.assertIn("Invalid input try again", self.mock_stdout.getvalue())

    def test_prompt_for_action_view_elections(self):
        self.mock_input.side_effect = ["1", "4"]
        with patch('project.show_elections_view') as mock_view:
            with self.assertRaises(SystemExit):
                project.prompt_for_action()
        mock_view.assert_called_once()
        self.assertIn("Viewing Elections...", self.mock_stdout.getvalue())

    def test_prompt_for_action_create_election(self):
        self.mock_input.side_effect = ["2", "4"]
        with patch('project.prompt_for_election_data') as mock_create:
            with self.assertRaises(SystemExit):
                project.prompt_for_action()
        mock_create.assert_called_once()
        self.assertIn("Creating Election...", self.mock_stdout.getvalue())

    def test_prompt_for_action_participate_in_election(self):
        self.mock_input.side_effect = ["3", "4"]
        with patch('project.prompt_for_vote') as mock_participate:
            with self.assertRaises(SystemExit):
                project.prompt_for_action()
        mock_participate.assert_called_once()
        self.assertIn("Participating in Election...", self.mock_stdout.getvalue())

    def test_prompt_for_election_data(self):
        with patch('project.create.get_election_title') as mock_title, \
             patch('project.create.get_options_number') as mock_options_number, \
             patch('project.create.get_options_details') as mock_options_details, \
             patch('project.create.get_is_self_voting') as mock_self_voting, \
             patch('project.create.get_is_public_election') as mock_public_election, \
             patch('project.create.get_allowed_voters') as mock_allowed_voters, \
             patch('project.create.create_election') as mock_create_election:
            
            mock_title.return_value = "Test Election"
            mock_options_number.return_value = 2
            mock_options_details.return_value = [("Option 1", "Details 1"), ("Option 2", "Details 2")]
            mock_self_voting.return_value = True
            mock_public_election.return_value = False
            mock_allowed_voters.return_value = ["voter1@example.com", "voter2@example.com"]
            
            project.user_email = "creator@example.com"
            project.prompt_for_election_data()
            
            mock_create_election.assert_called_once_with(
                "Test Election",
                [("Option 1", "Details 1"), ("Option 2", "Details 2")],
                True,
                False,
                "creator@example.com",
                ["voter1@example.com", "voter2@example.com"]
            )
        
        self.assertIn("Election successfully created!", self.mock_stdout.getvalue())

    def test_show_elections_view_no_elections(self):
        with patch('project.view.get_elections', return_value=[]):
            project.show_elections_view()
        self.assertIn("There are no polls / elections available at this time!", self.mock_stdout.getvalue())

    def test_show_elections_view_not_allowed(self):
        with patch('project.view.get_elections', return_value=["Election 1"]), \
             patch('project.view.get_chosen_election', return_value="Election 1"), \
             patch('project.view.is_allowed_to_view', return_value=False):
            project.user_email = "user@example.com"
            project.show_elections_view()
        self.assertNotIn("Election 1", self.mock_stdout.getvalue())

    def test_prompt_for_vote_no_elections(self):
        with patch('project.view.get_elections', return_value=[]):
            project.prompt_for_vote()
        self.assertEqual("", self.mock_stdout.getvalue().strip())

    def test_prompt_for_vote_not_allowed(self):
        with patch('project.view.get_elections', return_value=["Election 1"]), \
             patch('project.view.get_chosen_election', return_value="Election 1"), \
             patch('project.participate.is_allowed_to_vote', return_value=False):
            project.user_email = "user@example.com"
            project.prompt_for_vote()
        self.assertNotIn("Voted Successfully!", self.mock_stdout.getvalue())

    def test_prompt_for_vote_successful(self):
        with patch('project.view.get_elections', return_value=["Election 1"]), \
             patch('project.view.get_chosen_election', return_value="Election 1"), \
             patch('project.participate.is_allowed_to_vote', return_value=True), \
             patch('project.participate.get_candidates', return_value=[("Candidate 1", "Details 1")]), \
             patch('project.participate.prompt_for_option', return_value=1), \
             patch('project.participate.write_vote') as mock_write_vote, \
             patch('project.participate.update_vote_score') as mock_update_score:
            project.user_email = "user@example.com"
            project.prompt_for_vote()
            mock_write_vote.assert_called_once_with("Election 1", "user@example.com", "Candidate 1")
            mock_update_score.assert_called_once_with("Election 1", "Candidate 1")
        self.assertIn("Voted Successfully!", self.mock_stdout.getvalue())

    def test_main_function(self):
        with patch('project.start_app') as mock_start, \
             patch('project.prompt_for_action') as mock_prompt:
            project.main()
            mock_start.assert_called_once()
            mock_prompt.assert_called_once()

if __name__ == "__main__":
    unittest.main()