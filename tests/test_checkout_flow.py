import config
from pages.login_page import LoginPage


def test_checkout_flow(driver):
    login = LoginPage(driver)
    login.load()
    inventory = login.login_as(config.STANDARD_USER, config.STANDARD_PASSWORD)
    assert inventory.is_loaded()

    inventory.add_item("sauce-labs-backpack")
    cart = inventory.open_cart()
    assert cart.has_item_named("Sauce Labs Backpack")

    checkout = cart.checkout()
    checkout.fill_info("Test", "User", "12345")
    checkout.finish()
    assert checkout.is_complete()
