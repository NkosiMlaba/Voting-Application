import unittest
from io import StringIO
import sys
import io
from unittest.mock import patch
import project


class MyTestCase(unittest.TestCase):
    if 'unittest.util' in __import__('sys').modules:
    # Show full diff in self.assertEqual.
        __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999

    @patch("sys.stdin", StringIO('5\n5\n5\n2\n'))
    @patch("sys.stdout", new_callable = StringIO)
    def test_input_flow (self, mock_stdout):
        try:
            project.main()
        except EOFError:
            pass
        except SystemExit:
            pass

        output = mock_stdout.getvalue().strip()
        print(output)

        self.assertIn("", output)