import pytest
from config import BASE_URL, STANDARD_USER, LOCKED_OUT_USER, PASSWORD
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_TC01_standard_user_can_log_in(page):
    login = LoginPage(page)
    login.goto()
    login.login(STANDARD_USER, PASSWORD)
    page.wait_for_url("**/inventory.html")
    assert page.locator(".title").inner_text() == "Products"


def test_TC02_locked_out_user_sees_error(page):
    login = LoginPage(page)
    login.goto()
    login.login(LOCKED_OUT_USER, PASSWORD)
    assert "locked out" in login.error_text().lower()
    assert page.url.rstrip("/") == BASE_URL


def test_TC03_sort_price_low_to_high_checks_entire_list(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.sort("lohi")
    prices = inventory.prices()
    assert len(prices) > 1
    assert prices == sorted(prices), f"Prices are not ascending: {prices}"


def test_TC04_add_two_remove_one_updates_badge_and_cart(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_product("Sauce Labs Backpack")
    inventory.add_product("Sauce Labs Bike Light")
    assert inventory.badge_count() == 2

    inventory.remove_product("Sauce Labs Backpack")
    assert inventory.badge_count() == 1

    inventory.open_cart()
    cart = CartPage(logged_in_page)
    assert cart.names() == ["Sauce Labs Bike Light"]


def test_TC05_checkout_total_matches_subtotal_plus_tax_and_cart_is_empty(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_product("Sauce Labs Backpack")
    inventory.add_product("Sauce Labs Bike Light")
    inventory.open_cart()
    CartPage(logged_in_page).checkout()

    checkout = CheckoutPage(logged_in_page)
    checkout.fill_information("Aki", "Kumar", "641001")
    checkout.continue_checkout()

    subtotal, tax, total = checkout.amounts()
    assert total == pytest.approx(subtotal + tax, abs=0.011)

    checkout.finish()
    assert checkout.page.locator(checkout.complete_header).inner_text() == "Thank you for your order!"
    checkout.page.locator(checkout.back_home_button).click()
    assert checkout.page.wait_for_url("**/inventory.html") is None
    assert InventoryPage(checkout.page).badge_count() == 0


@pytest.mark.parametrize(
    ("first", "last", "postal", "expected_error"),
    [
        ("", "Kumar", "641001", "First Name is required"),
        ("Aki", "", "641001", "Last Name is required"),
        ("Aki", "Kumar", "", "Postal Code is required"),
    ],
    ids=["missing-first-name", "missing-last-name", "missing-postal-code"],
)
def test_TC06_TC07_TC08_checkout_required_fields(first, last, postal, expected_error, logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_product("Sauce Labs Backpack")
    inventory.open_cart()
    CartPage(logged_in_page).checkout()

    checkout = CheckoutPage(logged_in_page)
    checkout.fill_information(first, last, postal)
    checkout.continue_checkout()
    assert expected_error in checkout.page.locator(checkout.error_message).inner_text()


def test_TC09_logged_out_user_cannot_open_inventory_by_url(page):
    login = LoginPage(page)
    login.goto()
    login.login(STANDARD_USER, PASSWORD)
    page.wait_for_url("**/inventory.html")
    page.locator("#react-burger-menu-btn").click()
    page.locator("#logout_sidebar_link").click()
    page.wait_for_url(BASE_URL + "/")

    page.goto(f"{BASE_URL}/inventory.html")
    assert page.url.rstrip("/") == BASE_URL
    assert page.locator("#login-button").is_visible()
