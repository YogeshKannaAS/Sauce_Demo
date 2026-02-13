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


def test_checkout_flow_multiple_items(driver):
    login = LoginPage(driver)
    login.load()
    inventory = login.login_as(config.STANDARD_USER, config.STANDARD_PASSWORD)
    assert inventory.is_loaded()

    inventory.add_item("sauce-labs-backpack")
    cart = inventory.open_cart()
    assert cart.has_item_named("Sauce Labs Backpack")

    inventory = cart.continue_shopping()
    assert inventory.is_loaded()

    inventory.add_item("sauce-labs-bike-light")
    cart = inventory.open_cart()
    assert cart.has_item_named("Sauce Labs Backpack")
    assert cart.has_item_named("Sauce Labs Bike Light")

    checkout = cart.checkout()
    checkout.fill_info("Test", "User", "12345")
    checkout.finish()
    assert checkout.is_complete()
