import config
from pages.login_page import LoginPage


def _open_checkout(driver):
    login = LoginPage(driver)
    login.load()
    inventory = login.login_as(config.STANDARD_USER, config.STANDARD_PASSWORD)
    assert inventory.is_loaded()

    inventory.add_item("sauce-labs-backpack")
    cart = inventory.open_cart()
    assert cart.has_item_named("Sauce Labs Backpack")

    return cart.checkout()


def test_checkout_requires_first_name(driver):
    checkout = _open_checkout(driver)
    checkout.submit_info("", "User", "12345", expect_error=True)
    assert "First Name is required" in checkout.error_message()


def test_checkout_requires_last_name(driver):
    checkout = _open_checkout(driver)
    checkout.submit_info("Test", "", "12345", expect_error=True)
    assert "Last Name is required" in checkout.error_message()


def test_checkout_requires_postal_code(driver):
    checkout = _open_checkout(driver)
    checkout.submit_info("Test", "User", "", expect_error=True)
    assert "Postal Code is required" in checkout.error_message()
