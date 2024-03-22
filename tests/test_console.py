#!/usr/bin/python3
"""
Unit tests for the console using mock
"""

import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand


class TestHBNBCommand(unittest.TestCase):
    """Unit tests for the console using mock."""

    def setUp(self):
        """Set up the data to test."""
        self.cmd = HBNBCommand()

    def tearDown(self):
        """Destroy the data after testing."""
        pass

    @patch('sys.stdout', new_callable=StringIO)
    def test_quit_command(self, mock_stdout):
        """Test quit command."""
        self.assertTrue(self.cmd.onecmd("quit"))
        self.assertEqual(mock_stdout.getvalue(), '')

    @patch('sys.stdout', new_callable=StringIO)
    def test_EOF_command(self, mock_stdout):
        """Test end of file CTRL+D command."""
        self.assertTrue(self.cmd.onecmd("EOF"))
        self.assertEqual(mock_stdout.getvalue(), '\n')

    @patch('sys.stdout', new_callable=StringIO)
    def test_emptyline(self, mock_stdout):
        """Test empty line."""
        self.cmd.onecmd("")
        self.assertEqual(mock_stdout.getvalue(), '')

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_command(self, mock_stdout):
        """Test create function."""
        self.cmd.onecmd("create BaseModel")
        self.assertTrue(mock_stdout.getvalue().strip())

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_with_parameters(self, mock_stdout):
        """Test create with params."""
        self.cmd.onecmd('create State name="California"')
        output = mock_stdout.getvalue().strip()
        self.assertFalse(output.startswith("** Invalid parameter **"))

        mock_stdout.seek(0)
        mock_stdout.truncate(0)

        self.cmd.onecmd('create Place city_id="0001" user_id="0001" '
                        'name="My_little_house" number_rooms=4 '
                        'number_bathrooms=2 max_guest=10 price_by_night=300 '
                        'latitude=37.773972 longitude=-122.431297')
        output = mock_stdout.getvalue().strip()
        self.assertFalse(output.startswith(
            "76b65327-9e94-4632-b688-aaa22ab8a124"))

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_command(self, mock_stdout):
        """Test show function."""
        self.cmd.onecmd("show BaseModel")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** instance id missing **")

    @patch('sys.stdout', new_callable=StringIO)
    def test_destroy_command(self, mock_stdout):
        """Test destroy function."""
        self.cmd.onecmd("destroy BaseModel")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** instance id missing **")

    @patch('sys.stdout', new_callable=StringIO)
    def test_all_command(self, mock_stdout):
        """Test all function."""
        self.cmd.onecmd("all")
        self.assertTrue(mock_stdout.getvalue().strip())

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_command(self, mock_stdout):
        """Test update function."""
        self.cmd.onecmd("update BaseModel 1234 name John")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** no instance found **")


if __name__ == '__main__':
    unittest.main()
