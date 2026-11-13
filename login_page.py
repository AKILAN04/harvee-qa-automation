from pages.base_page import BasePage

class LoginPage(BasePage):
    username = "#user-name"
    password = "#password"
    login_button = "#login-button"
    error_message = "[data-test='error']"

    def goto(self):
        self.page.goto(self.base_url)

    def login(self, username, password):
        self.page.locator(self.username).fill(username)
        self.page.locator(self.password).fill(password)
        self.page.locator(self.login_button).click()

    def error_text(self):
        return self.page.locator(self.error_message).inner_text()
