import pytest

import config
from pages.login_page import LoginPage


LOGIN_USERS = [
    pytest.param("standard_user", "secret_sauce", True, id="standard_user"),
    pytest.param("problem_user", "secret_sauce", True, id="problem_user"),
    pytest.param("performance_glitch_user", "secret_sauce", True, id="performance_glitch_user"),
    pytest.param("error_user", "secret_sauce", True, id="error_user"),
    pytest.param("visual_user", "secret_sauce", True, id="visual_user"),
    pytest.param("locked_out_user", "secret_sauce", False, id="locked_out_user"),
    pytest.param("invalid_user_1", "secret_sauce", False, id="invalid_user_1"),
    pytest.param("invalid_user_2", "secret_sauce", False, id="invalid_user_2"),
    pytest.param("invalid_user_3", "wrong_password", False, id="invalid_user_3"),
    pytest.param("invalid_user_4", "wrong_password", False, id="invalid_user_4"),
    pytest.param("", "secret_sauce", False, id="blank_username"),
    pytest.param("standard_user", "", False, id="blank_password"),
    pytest.param("", "", False, id="blank_username_password"),
]


@pytest.mark.parametrize(
    "username,password,should_succeed",
    LOGIN_USERS,
)
def test_login_valid(driver, username, password, should_succeed):
    login = LoginPage(driver)
    login.load()
    inventory = login.login_as(username, password)
    if should_succeed:
        assert inventory.is_loaded()
    else:
        assert "Epic sadface" in login.error_message()
