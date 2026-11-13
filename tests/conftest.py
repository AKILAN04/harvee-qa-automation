import pytest
from config import BASE_URL, STANDARD_USER, PASSWORD
from pages.login_page import LoginPage

@pytest.fixture
def logged_in_page(page):
    login = LoginPage(page)
    login.goto()
    login.login(STANDARD_USER, PASSWORD)
    page.wait_for_url("**/inventory.html")
    return page
