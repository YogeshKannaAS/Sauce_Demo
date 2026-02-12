import pytest

import config
from pages.login_page import LoginPage


LOGIN_USERS = [
    ("standard_user", "secret_sauce", True),
    ("problem_user", "secret_sauce", True),
    ("performance_glitch_user", "secret_sauce", True),
    ("error_user", "secret_sauce", True),
    ("visual_user", "secret_sauce", True),
    ("locked_out_user", "secret_sauce", False),
    ("invalid_user_1", "secret_sauce", False),
    ("invalid_user_2", "secret_sauce", False),
    ("invalid_user_3", "wrong_password", False),
    ("invalid_user_4", "wrong_password", False),
]


@pytest.mark.parametrize(
    "username,password,should_succeed",
    LOGIN_USERS,
    ids=[u for u, _, _ in LOGIN_USERS],
)
def test_login_valid(driver, username, password, should_succeed):
    login = LoginPage(driver)
    login.load()
    inventory = login.login_as(username, password)
    if should_succeed:
        assert inventory.is_loaded()
    else:
        assert "Epic sadface" in login.error_message()
