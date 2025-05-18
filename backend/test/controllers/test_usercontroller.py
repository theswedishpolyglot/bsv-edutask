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

    def test_get_user_by_email_multiple_users_returns_first(self):
        user_data_1 = {'email': 'test@example.com', 'name': 'John'}
        user_data_2 = {'email': 'test@example.com', 'name': 'Jane'}
        self.mock_dao.find.return_value = [user_data_1, user_data_2]
        result = self.controller.get_user_by_email('test@example.com')
        assert result == user_data_1

    def test_get_user_by_email_multiple_users_prints_warning(self, capsys):
        user_data_1 = {'email': 'test@example.com', 'name': 'John'}
        user_data_2 = {'email': 'test@example.com', 'name': 'Jane'}
        self.mock_dao.find.return_value = [user_data_1, user_data_2]
        self.controller.get_user_by_email('test@example.com')
        captured = capsys.readouterr()
        assert "Warning" in captured.out or "multiple users" in captured.out.lower()

    def test_get_user_by_email_no_user(self):
        self.mock_dao.find.return_value = []
        result = self.controller.get_user_by_email('nobody@example.com')
        assert result is None

    def test_get_user_by_email_invalid_missing_at(self):
        with pytest.raises(ValueError):
            self.controller.get_user_by_email("userexample.com")

    def test_get_user_by_email_invalid_missing_domain(self):
        with pytest.raises(ValueError):
            self.controller.get_user_by_email("user@")

    def test_get_user_by_email_invalid_spaces(self):
        with pytest.raises(ValueError):
            self.controller.get_user_by_email("user @example.com")

    def test_get_user_by_email_invalid_empty_string(self):
        with pytest.raises(ValueError):
            self.controller.get_user_by_email("")

    def test_get_user_by_email_database_exception(self):
        self.mock_dao.find.side_effect = Exception("Database error")
        with pytest.raises(Exception):
            self.controller.get_user_by_email('test@example.com')
