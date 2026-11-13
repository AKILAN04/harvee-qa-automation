from pages.base_page import BasePage

class CheckoutPage(BasePage):
    first_name = "#first-name"
    last_name = "#last-name"
    postal_code = "#postal-code"
    continue_button = "#continue"
    cancel_button = "#cancel"
    finish_button = "#finish"
    error_message = "[data-test='error']"
    item_total = ".summary_subtotal_label"
    tax = ".summary_tax_label"
    total = ".summary_total_label"
    complete_header = ".complete-header"
    back_home_button = "#back-to-products"

    def fill_information(self, first, last, postal):
        self.page.locator(self.first_name).fill(first)
        self.page.locator(self.last_name).fill(last)
        self.page.locator(self.postal_code).fill(postal)

    def continue_checkout(self):
        self.page.locator(self.continue_button).click()

    def finish(self):
        self.page.locator(self.finish_button).click()

    def amounts(self):
        def amount(selector):
            text = self.page.locator(selector).inner_text()
            return float(text.split("$")[-1])
        return amount(self.item_total), amount(self.tax), amount(self.total)
