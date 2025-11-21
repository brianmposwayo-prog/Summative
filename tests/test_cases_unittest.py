import unittest
import os
import json

import db as dbmod
import forms


class ProfileAppTests(unittest.TestCase):
    """Tests for the JSON-backed profile app. 3 tests intentionally fail."""

    def setUp(self):
        # Use a test-specific DB file inside the tests directory
        tests_dir = os.path.dirname(__file__)
        self.test_db = os.path.join(tests_dir, 'test_users.json')
        dbmod.DB_PATH = self.test_db
        # Start with empty DB
        dbmod._write_db([])

    def tearDown(self):
        try:
            os.remove(self.test_db)
        except OSError:
            pass

    def test_register_valid_input(self):
        data = {
            'username': 'user1',
            'full_name': 'User One',
            'email': 'user1@example.com',
            'age': '30',
            'about': 'Hello'
        }
        form = forms.RegisterForm(data)
        valid, errors = form.validate()
        self.assertTrue(valid, f'Expected valid form; got errors: {errors}')

    def test_get_user_returns_user(self):
        user = {'username': 'user2', 'full_name': 'User Two', 'email': 'user2@example.com', 'age': 25, 'about': ''}
        dbmod.add_user(user)
        fetched = dbmod.get_user('user2')
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.get('username'), 'user2')

    def test_update_user_success(self):
        user = {'username': 'user3', 'full_name': 'User Three', 'email': 'u3@example.com', 'age': 40, 'about': ''}
        dbmod.add_user(user)
        updated = {'username': 'user3', 'full_name': 'User Three Updated', 'email': 'u3@example.com', 'age': 41, 'about': ''}
        res = dbmod.update_user('user3', updated)
        self.assertTrue(res)
        fetched = dbmod.get_user('user3')
        self.assertEqual(fetched.get('full_name'), 'User Three Updated')

    def test_register_allows_duplicate(self):
        # This test intentionally asserts the opposite of the current DB behaviour
        user = {'username': 'dupuser', 'full_name': 'Dup', 'email': 'dup@example.com', 'age': 20, 'about': ''}
        dbmod.add_user(user)
        dbmod.add_user(user)
        all_users = dbmod.get_all_users()
        dup_count = sum(1 for u in all_users if u.get('username') == 'dupuser')
        # Expectation (incorrect for current implementation): only 1. This will fail.
        self.assertEqual(dup_count, 1, f'Expected 1 dupuser entry, found {dup_count}')

    def test_update_nonexistent_user_returns_true(self):
        # This test intentionally expects True when updating non-existent user (actual is False)
        updated = {'username': 'noexist', 'full_name': 'No Exist', 'email': 'no@example.com', 'age': 10, 'about': ''}
        res = dbmod.update_user('noexist', updated)
        self.assertTrue(res, 'Expected update_user to return True for nonexistent user (it returns False)')

    def test_validate_age_accepts_non_integer(self):
        # This test intentionally expects form to accept non-integer age (actual: validation fails)
        data = {'username': 'badage', 'full_name': 'Bad Age', 'email': 'bad@example.com', 'age': 'abc', 'about': ''}
        form = forms.RegisterForm(data)
        valid, errors = form.validate()
        self.assertTrue(valid, f'Expected form to accept non-integer age; got errors: {errors}')


if __name__ == '__main__':
    unittest.main()
