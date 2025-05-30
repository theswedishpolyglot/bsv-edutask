import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

class TestUserController:

    def setup_method(self):
        self.mock_dao = MagicMock()
        self.controller = UserController(self.mock_dao)

    def test_get_user_by_email_single_user(self):
        user_data = {'email': 'test@example.com', 'name': 'John Doe'}
        self.mock_dao.find.return_value = [user_data]

        result = self.controller.get_user_by_email('test@example.com')
        assert result == user_data

        self.mock_dao.find.assert_called_once_with({'email': 'test@example.com'})

    def test_get_user_by_email_multiple_users_returns_first_user(self):
        user_data_1 = {'email': 'test@example.com', 'name': 'John Doe'}
        user_data_2 = {'email': 'test@example.com', 'name': 'Jane Smith'}
        self.mock_dao.find.return_value = [user_data_1, user_data_2]

        result = self.controller.get_user_by_email('test@example.com')
        assert result == user_data_1

    def test_get_user_by_email_multiple_users_find_called(self):
        user_data_1 = {'email': 'test@example.com', 'name': 'John Doe'}
        user_data_2 = {'email': 'test@example.com', 'name': 'Jane Smith'}
        self.mock_dao.find.return_value = [user_data_1, user_data_2]

        self.controller.get_user_by_email('test@example.com')
        self.mock_dao.find.assert_called_once_with({'email': 'test@example.com'})

    def test_get_user_by_email_multiple_users_prints_warning(self, capfd):
        user_data_1 = {'email': 'test@example.com', 'name': 'John Doe'}
        user_data_2 = {'email': 'test@example.com', 'name': 'Jane Smith'}
        self.mock_dao.find.return_value = [user_data_1, user_data_2]

        self.controller.get_user_by_email('test@example.com')
        out, _ = capfd.readouterr()
        assert 'Error: more than one user found with mail test@example.com' in out

    def test_get_user_by_email_no_user_returns_none(self):
        self.mock_dao.find.return_value = []

        result = self.controller.get_user_by_email('nonexistent@example.com')
        assert result is None

    def test_get_user_by_email_no_user_find_called(self):
        self.mock_dao.find.return_value = []

        self.controller.get_user_by_email('nonexistent@example.com')
        self.mock_dao.find.assert_called_once_with({'email': 'nonexistent@example.com'})

    def test_get_user_by_email_invalid_missing_at(self):
        with pytest.raises(ValueError):
            self.controller.get_user_by_email('invalidemail.com')

    def test_get_user_by_email_invalid_missing_domain(self):
        with pytest.raises(ValueError):
            self.controller.get_user_by_email('user@')

    def test_get_user_by_email_invalid_spaces(self):
        with pytest.raises(ValueError):
            self.controller.get_user_by_email('user @example.com')

    def test_get_user_by_email_invalid_empty(self):
        with pytest.raises(ValueError):
            self.controller.get_user_by_email('')

    def test_get_user_by_email_database_exception(self):
        self.mock_dao.find.side_effect = Exception("Database error")
        with pytest.raises(Exception):
            self.controller.get_user_by_email('test@example.com')
